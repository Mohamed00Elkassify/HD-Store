import { getTranslations } from "next-intl/server";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shield, RotateCcw, AlertTriangle, CheckCircle } from "lucide-react";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "warranty" });
  return {
    title: `${t("title")} — HD Store`,
    description: t("subtitle"),
  };
}

export default async function WarrantyReturnsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "warranty" });

  const returnConditions = [
    t("returnsCond1"),
    t("returnsCond2"),
    t("returnsCond3"),
    t("returnsCond4"),
    t("returnsCond5"),
    t("returnsCond6"),
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

      <div className="space-y-8">
        {/* Warranty */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-heading">
              <Shield className="h-5 w-5 text-primary" />
              {t("warrantyTitle")}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm leading-relaxed text-muted-foreground">
              {t("warrantyText1")}
            </p>
            <p className="text-sm leading-relaxed text-muted-foreground">
              {t("warrantyText2")}
            </p>
            <p className="text-sm leading-relaxed text-muted-foreground">
              {t("warrantyText3")}
            </p>
          </CardContent>
        </Card>

        {/* Returns */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 font-heading">
              <RotateCcw className="h-5 w-5 text-primary" />
              {t("returnsTitle")}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm leading-relaxed text-muted-foreground">
              {t("returnsText1")}
            </p>

            <div>
              <h4 className="mb-2 text-sm font-semibold">
                {t("returnsConditions")}
              </h4>
              <ul className="space-y-2">
                {returnConditions.map((cond, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 text-sm text-muted-foreground"
                  >
                    <CheckCircle className="mt-0.5 h-4 w-4 shrink-0 text-green-500" />
                    {cond}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="mb-2 text-sm font-semibold">
                {t("returnsProcess")}
              </h4>
              <p className="text-sm leading-relaxed text-muted-foreground">
                {t("returnsProcessText")}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Important Note */}
        <Card className="border-orange-200 bg-orange-50 dark:border-orange-900/50 dark:bg-orange-900/10">
          <CardContent className="flex gap-3 p-6">
            <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-orange-500" />
            <div>
              <h4 className="text-sm font-semibold">
                {t("note")}
              </h4>
              <p className="mt-1 text-sm text-muted-foreground">
                {t("noteText")}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
