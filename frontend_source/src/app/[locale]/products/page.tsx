import { getTranslations } from "next-intl/server";
import { ProductsClient } from "./products-client";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "products" });
  return {
    title: `${t("title")} — HD Store`,
    description: t("subtitle"),
  };
}

export default function ProductsPage() {
  return <ProductsClient />;
}
