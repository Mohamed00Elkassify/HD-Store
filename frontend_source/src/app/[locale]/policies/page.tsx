import { getTranslations } from "next-intl/server";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lock, FileText, Truck, Scale } from "lucide-react";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "policies" });
  return {
    title: `${t("title")} — HD Store`,
    description: t("subtitle"),
  };
}

export default async function PoliciesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "policies" });

  const sections = [
    {
      icon: Lock,
      title: t("privacy"),
      text: t("privacyText"),
    },
    {
      icon: FileText,
      title: t("terms"),
      text: t("termsText"),
    },
    {
      icon: Truck,
      title: t("shippingPolicy"),
      text: t("shippingText"),
    },
    {
      icon: Scale,
      title: t("legal"),
      text: t("legalText"),
    },
  ];

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center">
        <h1 className="font-heading text-3xl font-bold sm:text-4xl">
          {t("title")}
        </h1>
        <p className="mt-2 text-muted-foreground">
          {t("subtitle")}
        </p>
      </div>

      <div className="space-y-6">
        {sections.map((section) => (
          <Card key={section.title}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 font-heading text-lg">
                <section.icon className="h-5 w-5 text-primary" />
                {section.title}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed text-muted-foreground">
                {section.text}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
