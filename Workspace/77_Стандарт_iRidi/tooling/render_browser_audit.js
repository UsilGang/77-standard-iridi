"use strict";

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

async function main() {
  const input = process.argv[2];
  const output = process.argv[3];
  if (!input) throw new Error("Usage: node render_browser_audit.js <book.html> [report.json]");
  const htmlPath = path.resolve(input);
  const chromeCandidates = [
    process.env.STANDARD_BOOK_CHROME,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  ].filter(Boolean);
  const executablePath = chromeCandidates.find((candidate) => fs.existsSync(candidate));
  if (!executablePath) throw new Error("Chrome or Edge executable was not found");

  const browser = await chromium.launch({ headless: true, executablePath });
  const viewports = [
    { name: "desktop", width: 1600, height: 1000 },
    { name: "tablet", width: 1024, height: 900 },
    { name: "mobile", width: 640, height: 900 },
  ];
  const findings = [];
  const metrics = {};
  try {
    for (const viewport of viewports) {
      const page = await browser.newPage({ viewport });
      await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
      await page.evaluate(async () => {
        await Promise.all([...document.images].map((image) => image.decode().catch(() => null)));
      });
      const result = await page.evaluate(() => {
        const content = document.querySelector(".book-content");
        const contentRect = content ? content.getBoundingClientRect() : null;
        const brokenImages = [...document.images]
          .filter((image) => !image.complete || image.naturalWidth === 0 || image.naturalHeight === 0)
          .map((image) => image.getAttribute("src"));
        const overflow = [...document.querySelectorAll("main table, main img, main pre")]
          .filter((element) => {
            const rect = element.getBoundingClientRect();
            return contentRect && (rect.left < contentRect.left - 1 || rect.right > contentRect.right + 1);
          })
          .map((element) => ({ tag: element.tagName, text: (element.textContent || element.getAttribute("src") || "").trim().slice(0, 120) }));
        const headings = [...document.querySelectorAll("main h1, main h2, main h3")];
        const headingJumps = [];
        let previous = 1;
        for (const heading of headings) {
          const level = Number(heading.tagName.slice(1));
          if (level > previous + 1) headingJumps.push({ from: previous, to: level, text: heading.textContent.trim() });
          previous = level;
        }
        const ids = new Set([...document.querySelectorAll("[id]")].map((element) => element.id));
        const internalTargets = [...document.querySelectorAll("a[href^='#']")].map((link) => link.hash.slice(1));
        return {
          documentScrollWidth: document.documentElement.scrollWidth,
          viewportWidth: innerWidth,
          contentWidth: contentRect ? Math.round(contentRect.width) : null,
          tocCount: document.querySelectorAll("#std_toc").length,
          topicNavigationCount: document.querySelectorAll(".topic-navigation").length,
          tables: document.querySelectorAll("main table").length,
          headeredTables: document.querySelectorAll("main table.table-headered").length,
          headerlessTables: document.querySelectorAll("main table.table-headerless").length,
          images: document.querySelectorAll("main img").length,
          brokenImages,
          overflow,
          headingJumps,
          emptyHeadings: headings.filter((heading) => !heading.textContent.trim()).length,
          missingInternalTargets: [...new Set(internalTargets.filter((target) => !ids.has(target)))],
        };
      });
      metrics[viewport.name] = result;
      const add = (severity, checkId, details) => findings.push({ severity, check_id: checkId, viewport: viewport.name, details });
      if (result.tocCount !== 1) add("critical", "internal_navigation_integrity", `Expected one TOC, found ${result.tocCount}`);
      if (result.brokenImages.length) add("critical", "asset_count_digest_and_loadability", result.brokenImages);
      if (result.missingInternalTargets.length) add("critical", "topic_and_heading_addressing", result.missingInternalTargets);
      if (result.headingJumps.length || result.emptyHeadings) add("material", "heading_hierarchy", { jumps: result.headingJumps, empty: result.emptyHeadings });
      if (result.documentScrollWidth > result.viewportWidth + 1 || result.overflow.length) {
        add("material", "table_and_image_readability", {
          document_scroll_width: result.documentScrollWidth,
          viewport_width: result.viewportWidth,
          elements: result.overflow,
        });
      }
      if (viewport.name === "desktop" && result.contentWidth > 1040) add("material", "overflow_and_page_margins", result.contentWidth);
      await page.close();
    }
  } finally {
    await browser.close();
  }
  const summary = {
    critical: findings.filter((finding) => finding.severity === "critical").length,
    material: findings.filter((finding) => finding.severity === "material").length,
    cosmetic: findings.filter((finding) => finding.severity === "cosmetic").length,
  };
  const report = {
    schema_version: "1.0",
    audit_contract_uid: "std_render_parity_audit_contract_v1",
    input: htmlPath,
    status: summary.critical || summary.material ? "fail" : "pass",
    summary,
    findings,
    metrics,
  };
  const serialized = JSON.stringify(report, null, 2) + "\n";
  if (output) fs.writeFileSync(path.resolve(output), serialized, "utf8");
  process.stdout.write(serialized);
  process.exitCode = report.status === "pass" ? 0 : 2;
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
