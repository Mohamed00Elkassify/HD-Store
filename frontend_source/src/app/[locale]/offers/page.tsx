import { getTranslations } from "next-intl/server";
import { products } from "@/data/products";
import { ProductGrid } from "@/components/product-grid";
import { Badge } from "@/components/ui/badge";
import { Flame, TrendingUp, Timer } from "lucide-react";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "offers" });
  return {
    title: `${t("title")} — HD Store`,
    description: t("subtitle"),
  };
}

export default async function OffersPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale });

  const hotDeals = products.filter((p) =>
    p.tags?.includes("Hot Deal"),
  );
  const bestSellers = products.filter((p) =>
    p.tags?.includes("Best Seller"),
  );
  const limitedStock = products.filter((p) => p.inStock).slice(0, 4);

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-primary/10 via-background to-primary/5 py-12 sm:py-16">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <Badge className="mb-4 gap-1 px-3 py-1">
            <Flame className="h-3 w-3" />
            {t("offers.hotDeals")}
          </Badge>
          <h1 className="font-heading text-3xl font-bold sm:text-4xl">
            {t("offers.title")}
          </h1>
          <p className="mt-2 text-muted-foreground">
            {t("offers.subtitle")}
          </p>
        </div>
      </section>

      {/* Hot Deals */}
      <section className="py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-6 flex items-center gap-2">
            <Flame className="h-5 w-5 text-orange-500" />
            <h2 className="font-heading text-xl font-bold">
              {t("offers.hotDeals")}
            </h2>
          </div>
          <ProductGrid products={hotDeals} />
        </div>
      </section>

      {/* Best Sellers */}
      <section className="bg-muted/30 py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-6 flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            <h2 className="font-heading text-xl font-bold">
              {t("offers.bestSellers")}
            </h2>
          </div>
          <ProductGrid products={bestSellers} />
        </div>
      </section>

      {/* Limited Stock */}
      <section className="py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-6 flex items-center gap-2">
            <Timer className="h-5 w-5 text-red-500" />
            <h2 className="font-heading text-xl font-bold">
              {t("offers.limitedStock")}
            </h2>
          </div>
          <ProductGrid products={limitedStock} />
        </div>
      </section>
    </div>
  );
}
