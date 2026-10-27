import { test as base, expect } from "@playwright/test";
import { Sidebar } from "./fixtures/sidebar";

type SidebarFixtures = {
    sidebar: Sidebar;
};

const test = base.extend<SidebarFixtures>({
    sidebar: async ({ page }, use) => {
        const sidebar = new Sidebar(page);
        await use(sidebar);
    },
});

test.describe("Sidebar navigation", () => {
    test.beforeEach(async ({ page }) => {
        await page.goto("/");
    });

    test("Home link is visible", async ({ sidebar }) => {
        await expect(sidebar.sidebar).toBeVisible();
        await expect(sidebar.homeLink).toBeVisible();
    });

    test("Categories submenu expands and navigates to category page", async ({
        page,
        sidebar,
    }) => {

        // Expand the categories submenu
        await sidebar.categoriesToggle.click();
        await expect(sidebar.firstCategoryLink).toBeVisible();

        // Navigate to the first category page
        await sidebar.firstCategoryLink.click();
        await expect(page).toHaveURL(/\/category\//);

        // Category page shows a heading and sidebar remains
        await expect(sidebar.sidebar).toBeVisible();
        await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    });
});

