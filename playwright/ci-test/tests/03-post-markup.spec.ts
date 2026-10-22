import { test, expect } from "@playwright/test";

/**
 * The imported WordPress markup was translated to Bulma classes. These tests
 * check the result in a real browser, which is the only layer that shows the
 * rendering actually improved rather than just that the markup changed.
 */

const TABLE_POST = "/2024/07/14/plugin-update-june-2024/";
const EMBED_POST = "/2023/03/07/qgis-3.30-s-hertogenbosch-is-released/";
const GALLERY_POST = "/2018/11/05/report-back-on-the-20th-qgis-hackfest-in-zanzibar/";

test.describe("Imported post markup", () => {
    test("no WordPress classes survive anywhere on a post page", async ({ page }) => {
        await page.goto(TABLE_POST);
        for (const selector of [
            '[class*="wp-block"]',
            '[class*="wp-caption"]',
            '[class*="wp-image-"]',
            ".alignnone",
            ".size-large",
            ".size-full",
        ]) {
            await expect(page.locator(selector)).toHaveCount(0);
        }
    });

    test("no dead WordPress data attributes survive", async ({ page }) => {
        await page.goto(TABLE_POST);
        for (const selector of [
            "[data-attachment-id]",
            "[data-image-meta]",
            "[data-orig-file]",
            "[data-permalink]",
        ]) {
            await expect(page.locator(selector)).toHaveCount(0);
        }
    });

    test("tables are styled by Bulma and scroll instead of overflowing", async ({ page }) => {
        await page.goto(TABLE_POST);
        const table = page.locator(".content table.table").first();
        await expect(table).toBeVisible();

        // A wide table must scroll inside its own container, so the page body
        // never scrolls sideways.
        const container = page.locator(".content .table-container").first();
        await expect(container).toBeVisible();
        await expect(container).toHaveCSS("overflow-x", "auto");

        // Striping has to actually reach the cells.
        const cell = table.locator("td").first();
        await expect(cell).toHaveCSS("text-align", "left");
    });

    test("the page body never scrolls sideways on a narrow screen", async ({ page }) => {
        await page.setViewportSize({ width: 390, height: 844 });
        await page.goto(TABLE_POST);
        const overflows = await page.evaluate(
            () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
        );
        expect(overflows).toBe(false);
    });

    test("YouTube embeds render as a responsive 16:9 box", async ({ page }) => {
        await page.goto(EMBED_POST);
        const box = page.locator(".content .image.is-16by9").first();
        await expect(box).toBeVisible();

        // has-ratio is position:absolute, so it only works inside a ratio box.
        // If the box were on the wrong element the embed would collapse.
        const iframe = box.locator("iframe.has-ratio");
        await expect(iframe).toHaveCount(1);

        const size = await box.boundingBox();
        expect(size).not.toBeNull();
        expect(size!.height).toBeGreaterThan(100);
        expect(size!.width / size!.height).toBeCloseTo(16 / 9, 1);
    });

    test("the embed still points at the original video", async ({ page }) => {
        await page.goto(EMBED_POST);
        const src = await page
            .locator(".content .image.is-16by9 iframe")
            .first()
            .getAttribute("src");
        // The imported URL carries entity-escaped ampersands; the transform must
        // not have rewritten them into something YouTube cannot parse.
        expect(src).toContain("youtube.com/embed/");
        expect(src).toContain("q7O819lFKc4");
    });

    test("galleries render as a Bulma column grid with working images", async ({ page }) => {
        await page.goto(GALLERY_POST);
        // Scoped to .is-one-third on purpose: the page layout in
        // post-details.html also wraps the article in a .columns.is-multiline
        // inside .content, and its column is .is-9. Only the galleries use
        // .is-one-third, so this cannot pick up layout columns.
        const columns = page.locator(".column.is-one-third");
        await expect(columns).toHaveCount(6);

        // Every gallery image must actually load.
        const images = page.locator(".column.is-one-third figure.image img");
        const count = await images.count();
        expect(count).toBe(6);
        for (let i = 0; i < count; i++) {
            const loaded = await images.nth(i).evaluate(
                (img: HTMLImageElement) => img.complete && img.naturalWidth > 0,
            );
            expect(loaded, `gallery image ${i} failed to load`).toBe(true);
        }
    });

    test("each gallery thumbnail links to its full size original", async ({ page }) => {
        await page.goto(GALLERY_POST);
        const links = page.locator(".column.is-one-third figure.image a");
        await expect(links).toHaveCount(6);

        const href = await links.first().getAttribute("href");
        expect(href).toContain("/wp-content/uploads/");
        // The link must be the original, not the thumbnail derivative.
        expect(href).not.toContain("-thumb.");

        const response = await page.request.get(href!);
        expect(response.status()).toBe(200);
    });

    test("no image on a post page is broken", async ({ page }) => {
        for (const url of [TABLE_POST, EMBED_POST, GALLERY_POST]) {
            await page.goto(url);
            const broken = await page.evaluate(() =>
                Array.from(document.querySelectorAll("#content img, .content img"))
                    .filter((el) => {
                        const img = el as HTMLImageElement;
                        return img.complete && img.naturalWidth === 0;
                    })
                    .map((el) => (el as HTMLImageElement).currentSrc || el.getAttribute("src")),
            );
            expect(broken, `broken images on ${url}`).toEqual([]);
        }
    });
});
