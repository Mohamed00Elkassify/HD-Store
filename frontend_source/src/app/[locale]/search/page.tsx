"use client";

import { useSearchParams } from "next/navigation";
import { useTranslations, useLocale } from "next-intl";
import { products } from "@/data/products";
import { ProductGrid } from "@/components/product-grid";
import { EmptyState } from "@/components/empty-state";
import { Search } from "lucide-react";

export default function SearchPage() {
  const t = useTranslations();
  const locale = useLocale() as "ar" | "en";
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";

  const results = query.trim()
    ? products.filter((p) => {
        const q = query.toLowerCase();
        return (
          p.name[locale].toLowerCase().includes(q) ||
          p.brand.toLowerCase().includes(q) ||
          p.specs.cpu.toLowerCase().includes(q) ||
          p.specs.ram.toLowerCase().includes(q) ||
          p.specs.gpu.toLowerCase().includes(q) ||
          p.slug.includes(q)
        );
      })
    : [];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="font-heading text-2xl font-bold sm:text-3xl">
          {t("search.title")}
        </h1>
        {query && (
          <p className="mt-1 text-sm text-muted-foreground">
            {t("search.resultsFor")} &quot;{query}&quot; —{" "}
            {results.length} {t("common.results")}
          </p>
        )}
      </div>

      {results.length > 0 ? (
        <ProductGrid products={results} />
      ) : (
        <EmptyState
          icon={Search}
          title={
            query
              ? `${t("search.noResults")} "${query}"`
              : t("common.noResults")
          }
          description={t("search.suggestion")}
          actionLabel={t("nav.products")}
          actionHref="/products"
        />
      )}
    </div>
  );
}
