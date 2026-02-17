import { getTranslations } from "next-intl/server";
import Image from "next/image";
import { Link } from "@/i18n/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { products } from "@/data/products";
import { ProductGrid } from "@/components/product-grid";
import {
  ArrowRight,
  Shield,
  Truck,
  BadgeCheck,
  Banknote,
  ChevronRight,
  Laptop,
  Monitor,
  Gamepad2,
  Briefcase,
  DollarSign,
  Cable,
} from "lucide-react";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "home" });
  return {
    title: `HD Store — ${t("heroTitle")}`,
    description: t("heroSubtitle"),
  };
}

export default async function HomePage({
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
  const brands = ["Dell", "HP", "Lenovo"];

  const categories = [
    {
      icon: Laptop,
      title: t("home.catLaptops"),
      desc: t("home.catLaptopsDesc"),
      href: "/products" as const,
      color: "from-blue-500/20 to-blue-600/10",
      iconColor: "text-blue-500",
    },
    {
      icon: Monitor,
      title: t("home.catWorkstations"),
      desc: t("home.catWorkstationsDesc"),
      href: "/products" as const,
      color: "from-purple-500/20 to-purple-600/10",
      iconColor: "text-purple-500",
    },
    {
      icon: Gamepad2,
      title: t("home.catGaming"),
      desc: t("home.catGamingDesc"),
      href: "/products" as const,
      color: "from-red-500/20 to-red-600/10",
      iconColor: "text-red-500",
    },
    {
      icon: Briefcase,
      title: t("home.catBusiness"),
      desc: t("home.catBusinessDesc"),
      href: "/products" as const,
      color: "from-emerald-500/20 to-emerald-600/10",
      iconColor: "text-emerald-500",
    },
    {
      icon: DollarSign,
      title: t("home.catBudget"),
      desc: t("home.catBudgetDesc"),
      href: "/products" as const,
      color: "from-amber-500/20 to-amber-600/10",
      iconColor: "text-amber-500",
    },
    {
      icon: Cable,
      title: t("home.catAccessories"),
      desc: t("home.catAccessoriesDesc"),
      href: "/products" as const,
      color: "from-cyan-500/20 to-cyan-600/10",
      iconColor: "text-cyan-500",
    },
  ];

  return (
    <div>
      {/* ═══════════════ Hero Section ═══════════════ */}
      <section className="relative min-h-[520px] overflow-hidden sm:min-h-[580px] lg:min-h-[640px]">
        {/* Background Image */}
        <Image
          src="/images/hero-banner-new.png"
          alt=""
          fill
          className="object-cover object-center"
          priority
          sizes="100vw"
        />

        {/* Dark overlay gradient */}
        <div
          className="absolute inset-0 bg-gradient-to-t from-[#030a18]/95 via-[#030a18]/60 to-[#030a18]/40"
          aria-hidden
        />

        {/* Accent glow */}
        <div
          className="absolute -top-32 start-1/4 h-64 w-96 rounded-full bg-blue-500/15 blur-[120px]"
          aria-hidden
        />
        <div
          className="absolute -bottom-20 end-1/4 h-48 w-72 rounded-full bg-blue-400/10 blur-[100px]"
          aria-hidden
        />

        {/* Content */}
        <div className="relative mx-auto flex min-h-[520px] max-w-7xl flex-col justify-end px-4 pb-16 pt-24 sm:min-h-[580px] sm:px-6 lg:min-h-[640px] lg:justify-center lg:px-8 lg:pb-20">
          <div className="max-w-2xl">
            {/* Badge */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-400/30 bg-blue-500/10 px-4 py-1.5 backdrop-blur-sm">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-blue-500" />
              </span>
              <span className="text-xs font-medium text-blue-300">
                HD Store — Since 2008
              </span>
            </div>

            <h1
              className="text-4xl font-extrabold leading-[1.1] tracking-tight sm:text-5xl lg:text-[3.5rem] xl:text-6xl"
              style={{
                fontFamily: locale === "ar"
                  ? 'var(--font-cairo), system-ui, sans-serif'
                  : 'var(--font-heading), system-ui, sans-serif',
                textShadow: '0 2px 20px rgba(56, 120, 187, 0.3)',
              }}
            >
              <span className="bg-gradient-to-b from-white via-white to-blue-200/80 bg-clip-text text-transparent">
                {t("home.heroTitle")}
              </span>
            </h1>

            <p className="mt-5 max-w-lg text-base leading-relaxed text-blue-100/80 sm:text-lg">
              {t("home.heroSubtitle")}
            </p>

            {/* CTA Buttons */}
            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
              <Link href="/products">
                <Button
                  size="lg"
                  className="gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/25 transition-all hover:shadow-blue-500/40 hover:brightness-110"
                >
                  {t("home.heroCta")}
                  <ArrowRight className="h-4 w-4 rtl:rotate-180" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button
                  size="lg"
                  className="gap-2 border border-white/25 bg-white/10 text-white backdrop-blur-md transition-all hover:bg-white/20 hover:text-white"
                >
                  {t("home.contactCta")}
                  <ArrowRight className="h-4 w-4 rtl:rotate-180" />
                </Button>
              </Link>
              <Link href="/offers">
                <Button
                  size="lg"
                  variant="ghost"
                  className="gap-1 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200"
                >
                  {t("home.hotDeals")}
                  <ChevronRight className="h-4 w-4 rtl:rotate-180" />
                </Button>
              </Link>
            </div>
          </div>

          {/* Floating Stats (desktop) */}
          <div className="pointer-events-none absolute bottom-32 end-8 hidden flex-col gap-3 lg:flex">
            {[
              { value: "+17", label: locale === "ar" ? "سنة خبرة" : "Years" },
              { value: "+10K", label: locale === "ar" ? "جهاز مُباع" : "Sold" },
              { value: "+5K", label: locale === "ar" ? "عميل سعيد" : "Clients" },
            ].map((stat) => (
              <div
                key={stat.label}
                className="rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-center backdrop-blur-md"
              >
                <p className="font-heading text-xl font-bold text-white">
                  {stat.value}
                </p>
                <p className="text-[11px] text-blue-200/60">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════ Categories Section ═══════════════ */}
      <section className="relative -mt-12 z-10 py-4 sm:-mt-16 lg:-mt-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6 lg:gap-4">
            {categories.map((cat) => (
              <Link key={cat.title} href={cat.href}>
                <Card className="group relative overflow-hidden border-border/50 bg-card/80 backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5">
                  {/* Gradient background on hover */}
                  <div
                    className={`absolute inset-0 bg-gradient-to-br ${cat.color} opacity-0 transition-opacity duration-300 group-hover:opacity-100`}
                  />
                  <CardContent className="relative flex flex-col items-center gap-2.5 p-4 sm:p-5">
                    <div
                      className={`flex h-11 w-11 items-center justify-center rounded-xl bg-muted/80 transition-all duration-300 group-hover:scale-110 group-hover:bg-background/80 sm:h-12 sm:w-12`}
                    >
                      <cat.icon
                        className={`h-5 w-5 ${cat.iconColor} transition-transform duration-300 group-hover:scale-110 sm:h-6 sm:w-6`}
                      />
                    </div>
                    <h3 className="font-heading text-xs font-bold sm:text-sm">
                      {cat.title}
                    </h3>
                    <p className="line-clamp-2 text-center text-[10px] leading-tight text-muted-foreground sm:text-xs">
                      {cat.desc}
                    </p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Why Us */}
      <section className="py-12 sm:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center font-heading text-2xl font-bold sm:text-3xl">
            {t("home.whyUs")}
          </h2>
          <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                icon: BadgeCheck,
                title: t("home.whyInspected"),
                desc: t("home.whyInspectedDesc"),
              },
              {
                icon: Truck,
                title: t("home.whyDelivery"),
                desc: t("home.whyDeliveryDesc"),
              },
              {
                icon: Shield,
                title: t("home.whyWarranty"),
                desc: t("home.whyWarrantyDesc"),
              },
              {
                icon: Banknote,
                title: t("home.whyCod"),
                desc: t("home.whyCodDesc"),
              },
            ].map((item) => (
              <Card key={item.title} className="text-center">
                <CardContent className="flex flex-col items-center gap-3 p-6">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                    <item.icon className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-heading text-sm font-bold">
                    {item.title}
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    {item.desc}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Hot Deals */}
      {hotDeals.length > 0 && (
        <section className="py-12 sm:py-16">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mb-8 flex items-center justify-between">
              <h2 className="font-heading text-2xl font-bold">
                {t("home.hotDeals")}
              </h2>
              <Link href="/offers">
                <Button variant="ghost" size="sm" className="gap-1">
                  {t("common.viewAll")}
                  <ChevronRight className="h-4 w-4 rtl:rotate-180" />
                </Button>
              </Link>
            </div>
            <ProductGrid products={hotDeals.slice(0, 4)} />
          </div>
        </section>
      )}

      {/* Best Sellers */}
      {bestSellers.length > 0 && (
        <section className="bg-muted/30 py-12 sm:py-16">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mb-8 flex items-center justify-between">
              <h2 className="font-heading text-2xl font-bold">
                {t("home.bestSellers")}
              </h2>
              <Link href="/products">
                <Button variant="ghost" size="sm" className="gap-1">
                  {t("common.viewAll")}
                  <ChevronRight className="h-4 w-4 rtl:rotate-180" />
                </Button>
              </Link>
            </div>
            <ProductGrid products={bestSellers.slice(0, 4)} />
          </div>
        </section>
      )}

      {/* Shop by Brand */}
      <section className="py-12 sm:py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="mb-8 text-center font-heading text-2xl font-bold sm:text-3xl">
            {t("home.shopByBrand")}
          </h2>
          <div className="grid grid-cols-3 gap-4 sm:gap-6">
            {[
              { name: "Dell", logo: "/images/brands/dell.png" },
              { name: "HP", logo: "/images/brands/hp.png" },
              { name: "Lenovo", logo: "/images/brands/lenovo.png" },
            ].map((brand) => (
              <Link
                key={brand.name}
                href={`/products?brand=${brand.name}`}
              >
                <Card className="group overflow-hidden border-border/60 transition-all duration-300 hover:-translate-y-1 hover:border-primary/30 hover:shadow-xl hover:shadow-primary/10">
                  <CardContent className="flex flex-col items-center gap-4 p-6 sm:p-8">
                    <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl bg-muted/50 p-2 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary/5 sm:h-20 sm:w-20 sm:p-3">
                      <Image
                        src={brand.logo}
                        alt={brand.name}
                        width={64}
                        height={64}
                        className="h-full w-full object-contain"
                      />
                    </div>
                    <span className="font-heading text-sm font-bold transition-colors group-hover:text-primary sm:text-lg">
                      {brand.name}
                    </span>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-primary py-12 text-primary-foreground sm:py-16">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <h2 className="font-heading text-2xl font-bold sm:text-3xl">
            {t("home.viewAllProducts")}
          </h2>
          <p className="mt-2 text-primary-foreground/80">
            {t("home.featuredSubtitle")}
          </p>
          <Link href="/products">
            <Button
              variant="secondary"
              size="lg"
              className="mt-6 gap-2"
            >
              {t("home.heroCta")}
              <ArrowRight className="h-4 w-4 rtl:rotate-180" />
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
