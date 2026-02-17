"use client";

import { useTranslations, useLocale } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useCartStore } from "@/store/cart";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { QuantitySelector } from "@/components/quantity-selector";
import { EmptyState } from "@/components/empty-state";
import { formatPrice } from "@/lib/constants";
import { toast } from "sonner";
import {
  Trash2,
  Laptop,
  ShoppingCart,
  ArrowRight,
} from "lucide-react";
import { useEffect, useState } from "react";

export default function CartPage() {
  const t = useTranslations();
  const locale = useLocale() as "ar" | "en";
  const items = useCartStore((s) => s.items);
  const removeItem = useCartStore((s) => s.removeItem);
  const updateQuantity = useCartStore((s) => s.updateQuantity);
  const getTotal = useCartStore((s) => s.getTotal);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  if (items.length === 0) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <EmptyState
          icon={ShoppingCart}
          title={t("cart.empty")}
          description={t("cart.emptyDesc")}
          actionLabel={t("cart.continueShopping")}
          actionHref="/products"
        />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="mb-8 font-heading text-2xl font-bold sm:text-3xl">
        {t("cart.title")}
      </h1>

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Items */}
        <div className="space-y-4 lg:col-span-2">
          {items.map((item) => (
            <Card key={item.product.id}>
              <CardContent className="flex gap-4 p-4">
                {/* Image placeholder */}
                <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-lg bg-muted">
                  <Laptop className="h-8 w-8 text-muted-foreground/40" />
                </div>

                <div className="min-w-0 flex-1 space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <Link
                      href={`/products/${item.product.slug}`}
                      className="text-sm font-semibold hover:text-primary"
                    >
                      {item.product.name[locale]}
                    </Link>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 shrink-0 text-muted-foreground hover:text-destructive"
                      onClick={() => {
                        removeItem(item.product.id);
                        toast.success(t("cart.itemRemoved"));
                      }}
                      aria-label={t("common.remove")}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>

                  <p className="text-xs text-muted-foreground">
                    {item.product.brand} — {t("common.grade")} {item.product.grade}
                  </p>

                  <div className="flex items-center justify-between">
                    <QuantitySelector
                      quantity={item.quantity}
                      onChange={(q) => {
                        updateQuantity(item.product.id, q);
                        toast.success(t("cart.itemUpdated"));
                      }}
                    />
                    <span className="text-sm font-bold text-primary">
                      {formatPrice(
                        item.product.priceEGP * item.quantity,
                      )}{" "}
                      {t("common.egp")}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Summary */}
        <div>
          <Card className="sticky top-20">
            <CardHeader>
              <CardTitle className="font-heading text-lg">
                {t("cart.orderSummary")}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">
                  {t("common.subtotal")}
                </span>
                <span className="font-semibold">
                  {formatPrice(getTotal())} {t("common.egp")}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">
                  {t("common.shipping")}
                </span>
                <span className="text-xs text-muted-foreground">
                  {t("cart.shippingNote")}
                </span>
              </div>
              <Separator />
              <div className="flex justify-between">
                <span className="font-semibold">
                  {t("common.total")}
                </span>
                <span className="text-lg font-bold text-primary">
                  {formatPrice(getTotal())} {t("common.egp")}
                </span>
              </div>
              <Link href="/checkout" className="block">
                <Button className="w-full gap-2" size="lg">
                  {t("cart.proceedCheckout")}
                  <ArrowRight className="h-4 w-4 rtl:rotate-180" />
                </Button>
              </Link>
              <Link href="/products" className="block">
                <Button
                  variant="ghost"
                  className="w-full"
                  size="sm"
                >
                  {t("cart.continueShopping")}
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
