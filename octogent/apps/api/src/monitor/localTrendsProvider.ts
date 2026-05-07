import { readFile } from "node:fs/promises";
import { join } from "node:path";
import type {
  MonitorPost,
  MonitorProviderAdapter,
  MonitorProviderId,
} from "./types";

export class LocalTrendsProvider implements MonitorProviderAdapter {
  public providerId: MonitorProviderId = "x"; // Mantemos 'x' para compatibilidade com o frontend atual
  private workspaceCwd: string;

  constructor(workspaceCwd: string) {
    this.workspaceCwd = workspaceCwd;
  }

  async fetchRecentPosts(): Promise<MonitorPost[]> {
    const filePath = join(this.workspaceCwd, "outputs", "trends_data.json");
    try {
      const content = await readFile(filePath, "utf-8");
      const data = JSON.parse(content);
      const posts: MonitorPost[] = [];

      if (data.google_news) {
        for (const item of data.google_news) {
          posts.push({
            source: "google-news",
            id: item.link,
            text: item.title,
            author: item.source,
            createdAt: item.published,
            likeCount: 0,
            permalink: item.link,
            matchedQueryTerm: "News"
          });
        }
      }
      return posts;
    } catch (e) {
      console.error("LocalTrendsProvider error:", e);
      return [];
    }
  }

  async fetchUsage() {
    return {
      cap: 100,
      used: 0,
      remaining: 100,
      window7d: 0,
      resets: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    };
  }

  summarizeCredentials() {
    return { status: "Local Monitor Active" };
  }

  saveCredentials(input: any) {
    return { credentials: { token: "local" } };
  }

  async validateCredentials(): Promise<{ ok: boolean }> {
    return { ok: true };
  }
}

export const createLocalTrendsProvider = (workspaceCwd: string) => new LocalTrendsProvider(workspaceCwd);
