import type { Metadata } from "next";
import { Newspaper } from "lucide-react";

import { PostFilter } from "@/components/news/PostFilter";
import { Container, EmptyState, PageHeader, Section } from "@/components/ui";
import { getCategories, getPosts } from "@/lib/api";

export const metadata: Metadata = {
  title: "News & Stories",
  description:
    "News, announcements, impact stories and podcasts from Simply Green Organization's environmental work in Tanzania.",
  alternates: { canonical: "/news" },
};

export default async function NewsPage() {
  const [posts, categories] = await Promise.all([
    getPosts({ pageSize: 60 }),
    getCategories(),
  ]);

  return (
    <>
      <PageHeader
        eyebrow="News & events"
        title="News and stories"
        description="What we are learning, publishing and seeing change."
      />

      <Section>
        <Container>
          {posts.results.length === 0 ? (
            <EmptyState
              icon={<Newspaper className="h-10 w-10" />}
              title="No articles published yet"
              description="Posts written in the admin will appear here."
            />
          ) : (
            <PostFilter posts={posts.results} categories={categories} />
          )}
        </Container>
      </Section>
    </>
  );
}
