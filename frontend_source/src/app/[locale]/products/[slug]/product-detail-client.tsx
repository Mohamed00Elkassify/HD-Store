"use client";

import { Product } from "@/types/product";
import { useTranslations, useLocale } from "next-intl";
import { Link, useRouter } from "@/i18n/navigation";
import { useCartStore } from "@/store/cart";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { ProductGrid } from "@/components/product-grid";
import { formatPrice } from "@/lib/constants";
import { toast } from "sonner";
import {
  ShoppingCart,
  Zap,
  Cpu,
  HardDrive,
  Monitor,
  Battery,
  Shield,
  Keyboard,
  MemoryStick,
  ChevronRight,
  Home,
} from "lucide-react";
import { ProductImage } from "@/components/product-image";

interface Props {
  product: Product;
  related: Product[];
}

export function ProductDetailClient({ product, related }: Props) {
  const t = useTranslations();
  const locale = useLocale() as "ar" | "en";
  const router = useRouter();
  const addItem = useCartStore((s) => s.addItem);

  const handleAddToCart = () => {
    addItem(product);
    toast.success(t("cart.itemAdded"));
  };

  const handleBuyNow = () => {
    addItem(product);
    router.push("/checkout");
  };

  const specItems = [
    { icon: Cpu, label: t("product.cpu"), value: product.specs.cpu },
    { icon: MemoryStick, label: t("product.ram"), value: product.specs.ram },
    { icon: HardDrive, label: t("product.storage"), value: product.specs.storage },
    { icon: Monitor, label: t("product.gpu"), value: product.specs.gpu },
    { icon: Monitor, label: t("product.screen"), value: product.specs.screen },
    { icon: Battery, label: t("product.battery"), value: product.specs.battery },
    { icon: Shield, label: t("product.warranty"), value: product.specs.warranty },
    {
      icon: Keyboard,
      label: t("product.keyboard"),
      value: t(`keyboardLayouts.${product.keyboardLayout}`),
    },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Breadcrumbs */}
      <nav className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
        <Link
          href="/"
          className="hover:text-foreground"
        >
          <Home className="h-3.5 w-3.5" />
        </Link>
        <ChevronRight className="h-3 w-3 rtl:rotate-180" />
        <Link
          href="/products"
          className="hover:text-foreground"
        >
          {t("nav.products")}
        </Link>
        <ChevronRight className="h-3 w-3 rtl:rotate-180" />
        <span className="truncate text-foreground">
          {product.name[locale]}
        </span>
      </nav>

      {/* Main section */}
      <div className="grid gap-8 lg:grid-cols-2">
        {/* Image */}
        <div className="relative aspect-square w-full overflow-hidden rounded-xl">
          <ProductImage
            src={product.images?.[0]}
            alt={product.name[locale]}
            className="rounded-xl"
            fill
            sizes="(max-width: 1024px) 100vw, 50vw"
            priority
          />
        </div>

        {/* Info */}
        <div className="space-y-6">
          {/* Brand */}
          <p className="text-sm font-medium text-muted-foreground">
            {product.brand}
          </p>

          {/* Title */}
          <h1 className="font-heading text-2xl font-bold sm:text-3xl">
            {product.name[locale]}
          </h1>

          {/* Badges */}
          <div className="flex flex-wrap gap-2">
            <Badge
              variant={product.inStock ? "default" : "destructive"}
            >
              {product.inStock
                ? t("common.inStock")
                : t("common.outOfStock")}
            </Badge>
            <Badge variant="secondary">
              {t("common.grade")} {product.grade}
            </Badge>
            <Badge variant="secondary">
              {t(`conditions.${product.condition}`)}
            </Badge>
            <Badge
              variant={
                product.includesCharger ? "default" : "secondary"
              }
            >
              {product.includesCharger
                ? t("common.includesCharger")
                : t("common.noCharger")}
            </Badge>
          </div>

          {/* Price */}
          <div className="flex items-baseline gap-3">
            <span className="text-3xl font-bold text-primary">
              {formatPrice(product.priceEGP)}
            </span>
            <span className="text-lg text-muted-foreground">
              {t("common.egp")}
            </span>
            {product.oldPriceEGP && (
              <span className="text-lg text-muted-foreground line-through">
                {formatPrice(product.oldPriceEGP)} {t("common.egp")}
              </span>
            )}
          </div>

          {/* CTAs */}
          <div className="flex flex-col gap-3 sm:flex-row">
            <Button
              size="lg"
              className="flex-1 gap-2"
              onClick={handleAddToCart}
              disabled={!product.inStock}
            >
              <ShoppingCart className="h-4 w-4" />
              {t("common.addToCart")}
            </Button>
            <Button
              size="lg"
              variant="secondary"
              className="flex-1 gap-2"
              onClick={handleBuyNow}
              disabled={!product.inStock}
            >
              <Zap className="h-4 w-4" />
              {t("common.buyNow")}
            </Button>
          </div>

          <Separator />

          {/* Quick specs grid */}
          <div className="grid grid-cols-2 gap-3">
            {specItems.slice(0, 6).map((item) => (
              <div
                key={item.label}
                className="flex items-start gap-2 rounded-lg bg-muted/50 p-3"
              >
                <item.icon className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
                <div className="min-w-0">
                  <p className="text-xs text-muted-foreground">
                    {item.label}
                  </p>
                  <p className="truncate text-sm font-medium">
                    {item.value}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mt-12">
        <Tabs defaultValue="specs">
          <TabsList className="w-full justify-start">
            <TabsTrigger value="specs">
              {t("product.specifications")}
            </TabsTrigger>
            <TabsTrigger value="shipping">
              {t("product.shippingDelivery")}
            </TabsTrigger>
            <TabsTrigger value="warranty">
              {t("product.warrantyReturns")}
            </TabsTrigger>
          </TabsList>

          <TabsContent value="specs" className="mt-6">
            <Card>
              <CardContent className="p-6">
                <div className="grid gap-4 sm:grid-cols-2">
                  {specItems.map((item) => (
                    <div
                      key={item.label}
                      className="flex items-start gap-3"
                    >
                      <item.icon className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
                      <div>
                        <p className="text-xs text-muted-foreground">
                          {item.label}
                        </p>
                        <p className="text-sm font-medium">
                          {item.value}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="shipping" className="mt-6">
            <Card>
              <CardContent className="p-6">
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {t("product.shippingInfo")}
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="warranty" className="mt-6">
            <Card>
              <CardContent className="space-y-4 p-6">
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {t("product.warrantyInfo")}
                </p>
                <Link href="/warranty-returns">
                  <Button variant="link" className="h-auto p-0">
                    {t("product.readMore")}
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* Related */}
      {related.length > 0 && (
        <div className="mt-12">
          <h2 className="mb-6 font-heading text-xl font-bold">
            {t("product.relatedProducts")}
          </h2>
          <ProductGrid products={related} />
        </div>
      )}
    </div>
  );
}
