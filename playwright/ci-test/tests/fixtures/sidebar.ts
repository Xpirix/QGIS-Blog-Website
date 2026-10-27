import type { Page, Locator } from "@playwright/test";

export class Sidebar {
    public readonly sidebar: Locator;
    public readonly homeLink: Locator;
    /** Toggle button that expands the authors sub-list (no href). */
    public readonly categoriesToggle: Locator;
    /** First author link inside the (collapsed) authors sub-list. */
    public readonly firstAuthorLink: Locator;
    /** First category link inside the (collapsed) categories sub-list. */
    public readonly firstCategoryLink: Locator;

    constructor(public readonly page: Page) {
        this.sidebar = this.page.locator("#sidebar");
        this.homeLink = this.sidebar.getByRole("link", { name: "Home" });
        this.categoriesToggle = this.sidebar
            .locator(".has-child")
            .filter({ hasText: "Categories" })
            .locator("a.icon-text");
        this.firstAuthorLink = this.sidebar
            .locator("#authors li a")
            .first();
        this.firstCategoryLink = this.sidebar
            .locator("#categories li a")
            .first();
    }
}
