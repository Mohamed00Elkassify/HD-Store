import { getTranslations } from "next-intl/server";
import { Card, CardContent } from "@/components/ui/card";
import {
  BadgeCheck,
  Eye,
  Headphones,
  Laptop,
  Users,
  Calendar,
} from "lucide-react";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "about" });
  return {
    title: `${t("title")} — HD Store`,
    description: t("subtitle"),
  };
}

export default async function AboutPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "about" });

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-12 text-center">
        <h1 className="font-heading text-3xl font-bold sm:text-4xl">
          {t("title")}
        </h1>
        <p className="mt-2 text-muted-foreground">{t("subtitle")}</p>
      </div>

      {/* Stats */}
      <div className="mb-12 grid grid-cols-3 gap-4">
        {[
          {
            icon: Calendar,
            val: t("stats.years"),
            desc: t("stats.yearsDesc"),
          },
          {
            icon: Laptop,
            val: t("stats.laptops"),
            desc: t("stats.laptopsDesc"),
          },
          {
            icon: Users,
            val: t("stats.customers"),
            desc: t("stats.customersDesc"),
          },
        ].map((s) => (
          <Card key={s.desc} className="text-center">
            <CardContent className="flex flex-col items-center gap-2 p-6">
              <s.icon className="h-6 w-6 text-primary" />
              <span className="font-heading text-xl font-bold text-primary sm:text-2xl">
                {s.val}
              </span>
              <span className="text-xs text-muted-foreground">
                {s.desc}
              </span>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Story */}
      <div className="mb-12 space-y-4">
        <h2 className="font-heading text-xl font-bold">
          {t("story")}
        </h2>
        <p className="leading-relaxed text-muted-foreground">
          {t("storyText")}
        </p>
      </div>

      {/* Mission */}
      <div className="mb-12 space-y-4">
        <h2 className="font-heading text-xl font-bold">
          {t("mission")}
        </h2>
        <p className="leading-relaxed text-muted-foreground">
          {t("missionText")}
        </p>
      </div>

      {/* Values */}
      <div>
        <h2 className="mb-6 font-heading text-xl font-bold">
          {t("values")}
        </h2>
        <div className="grid gap-6 sm:grid-cols-3">
          {[
            {
              icon: BadgeCheck,
              title: t("quality"),
              desc: t("qualityDesc"),
            },
            {
              icon: Eye,
              title: t("transparency"),
              desc: t("transparencyDesc"),
            },
            {
              icon: Headphones,
              title: t("support"),
              desc: t("supportDesc"),
            },
          ].map((v) => (
            <Card key={v.title}>
              <CardContent className="flex flex-col items-center gap-3 p-6 text-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                  <v.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="font-heading text-sm font-bold">
                  {v.title}
                </h3>
                <p className="text-xs text-muted-foreground">
                  {v.desc}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
