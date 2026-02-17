import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { products } from "@/data/products";
import { ProductDetailClient } from "./product-detail-client";

export async function generateStaticParams() {
  return products.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  const product = products.find((p) => p.slug === slug);
  if (!product) return {};
  const loc = locale as "ar" | "en";
  return {
    title: `${product.name[loc]} — HD Store`,
    description: product.shortSpecs[loc].join(" | "),
  };
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { slug } = await params;
  const product = products.find((p) => p.slug === slug);
  if (!product) notFound();

  const related = products
    .filter(
      (p) =>
        p.id !== product.id &&
        (p.brand === product.brand ||
          Math.abs(p.priceEGP - product.priceEGP) < 3000),
    )
    .slice(0, 4);

  return (
    <ProductDetailClient product={product} related={related} />
  );
}
