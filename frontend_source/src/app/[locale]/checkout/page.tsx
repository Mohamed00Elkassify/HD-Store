"use client";

import { useState, useEffect } from "react";
import { useTranslations, useLocale } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCartStore } from "@/store/cart";
import {
  checkoutSchema,
  CheckoutFormValues,
} from "@/lib/checkout-schema";
import { assiutCenters } from "@/data/products";
import { getWhatsAppLink, formatPrice, WHATSAPP_DISPLAY } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { EmptyState } from "@/components/empty-state";
import { toast } from "sonner";
import {
  ShoppingCart,
  CheckCircle,
  MessageCircle,
  Copy,
  Banknote,
  Laptop,
} from "lucide-react";

export default function CheckoutPage() {
  const t = useTranslations();
  const locale = useLocale() as "ar" | "en";
  const items = useCartStore((s) => s.items);
  const getTotal = useCartStore((s) => s.getTotal);
  const clearCart = useCartStore((s) => s.clearCart);
  const [mounted, setMounted] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [orderMessage, setOrderMessage] = useState("");

  useEffect(() => {
    setMounted(true);
  }, []);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<CheckoutFormValues>({
    resolver: zodResolver(checkoutSchema),
  });

  if (!mounted) return null;

  if (items.length === 0 && !submitted) {
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

  const onSubmit = (data: CheckoutFormValues) => {
    const center = assiutCenters.find(
      (c) => c.value === data.assiutCenter,
    );
    const centerName = center
      ? center.label[locale]
      : data.assiutCenter;

    let msg = locale === "ar"
      ? "🛒 *طلب جديد من موقع HD Store*\n\n"
      : "🛒 *New Order from HD Store Website*\n\n";

    msg += locale === "ar"
      ? `👤 *الاسم:* ${data.fullName}\n📱 *الهاتف:* ${data.phone}\n📍 *المركز:* ${centerName}\n🏠 *العنوان:* ${data.addressDetails}\n`
      : `👤 *Name:* ${data.fullName}\n📱 *Phone:* ${data.phone}\n📍 *Center:* ${centerName}\n🏠 *Address:* ${data.addressDetails}\n`;

    if (data.landmark) {
      msg += locale === "ar"
        ? `📌 *علامة مميزة:* ${data.landmark}\n`
        : `📌 *Landmark:* ${data.landmark}\n`;
    }
    if (data.notes) {
      msg += locale === "ar"
        ? `📝 *ملاحظات:* ${data.notes}\n`
        : `📝 *Notes:* ${data.notes}\n`;
    }

    msg += "\n---\n";
    msg += locale === "ar" ? "📦 *المنتجات:*\n" : "📦 *Items:*\n";

    items.forEach((item) => {
      msg += `• ${item.product.name[locale]} × ${item.quantity} = ${formatPrice(item.product.priceEGP * item.quantity)} ${locale === "ar" ? "ج.م" : "EGP"}\n`;
    });

    msg += "\n---\n";
    msg += locale === "ar"
      ? `💰 *الإجمالي:* ${formatPrice(getTotal())} ج.م\n💵 *طريقة الدفع:* الدفع عند الاستلام`
      : `💰 *Total:* ${formatPrice(getTotal())} EGP\n💵 *Payment:* Cash on Delivery`;

    setOrderMessage(msg);
    setSubmitted(true);
    clearCart();
  };

  if (submitted) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="text-center">
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h1 className="font-heading text-2xl font-bold">
            {t("checkout.success.title")}
          </h1>
          <p className="mt-2 text-muted-foreground">
            {t("checkout.success.subtitle")}
          </p>

          <div className="mt-8 space-y-4">
            <a
              href={getWhatsAppLink(orderMessage)}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button size="lg" className="w-full gap-2">
                <MessageCircle className="h-5 w-5" />
                {t("checkout.success.confirmWhatsApp")}
              </Button>
            </a>

            <Button
              variant="outline"
              size="lg"
              className="w-full gap-2"
              onClick={() => {
                navigator.clipboard.writeText(orderMessage);
                toast.success(t("common.copied"));
              }}
            >
              <Copy className="h-4 w-4" />
              {t("checkout.success.copyMessage")}
            </Button>

            <Link href="/products">
              <Button variant="ghost" size="lg" className="w-full">
                {t("checkout.success.newOrder")}
              </Button>
            </Link>
          </div>

          {/* Order message preview */}
          <Card className="mt-8 text-start">
            <CardHeader>
              <CardTitle className="text-sm">
                {t("checkout.success.orderMessage")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="whitespace-pre-wrap text-xs text-muted-foreground" dir="auto">
                {orderMessage}
              </pre>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="font-heading text-2xl font-bold sm:text-3xl">
          {t("checkout.title")}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {t("checkout.subtitle")}
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="grid gap-8 lg:grid-cols-3">
          {/* Form */}
          <div className="space-y-6 lg:col-span-2">
            {/* Payment method badge */}
            <Card>
              <CardContent className="flex items-center gap-3 p-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
                  <Banknote className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold">
                    {t("checkout.cod")}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {t("checkout.codDesc")}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Form fields */}
            <Card>
              <CardContent className="space-y-4 p-6">
                {/* Full Name */}
                <div className="space-y-2">
                  <Label htmlFor="fullName">
                    {t("checkout.form.fullName")} *
                  </Label>
                  <Input
                    id="fullName"
                    {...register("fullName")}
                    placeholder={t("checkout.form.fullNamePlaceholder")}
                  />
                  {errors.fullName && (
                    <p className="text-xs text-destructive">
                      {t(`checkout.${errors.fullName.message}`)}
                    </p>
                  )}
                </div>

                {/* Phone */}
                <div className="space-y-2">
                  <Label htmlFor="phone">
                    {t("checkout.form.phone")} *
                  </Label>
                  <Input
                    id="phone"
                    {...register("phone")}
                    placeholder={t("checkout.form.phonePlaceholder")}
                    type="tel"
                    dir="ltr"
                  />
                  {errors.phone && (
                    <p className="text-xs text-destructive">
                      {t(`checkout.${errors.phone.message}`)}
                    </p>
                  )}
                </div>

                {/* Center */}
                <div className="space-y-2">
                  <Label>
                    {t("checkout.form.assiutCenter")} *
                  </Label>
                  <Select
                    onValueChange={(v) =>
                      setValue("assiutCenter", v, {
                        shouldValidate: true,
                      })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue
                        placeholder={t(
                          "checkout.form.assiutCenterPlaceholder",
                        )}
                      />
                    </SelectTrigger>
                    <SelectContent>
                      {assiutCenters.map((center) => (
                        <SelectItem
                          key={center.value}
                          value={center.value}
                        >
                          {center.label[locale]}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {errors.assiutCenter && (
                    <p className="text-xs text-destructive">
                      {t(`checkout.${errors.assiutCenter.message}`)}
                    </p>
                  )}
                </div>

                {/* Address */}
                <div className="space-y-2">
                  <Label htmlFor="addressDetails">
                    {t("checkout.form.addressDetails")} *
                  </Label>
                  <Input
                    id="addressDetails"
                    {...register("addressDetails")}
                    placeholder={t(
                      "checkout.form.addressDetailsPlaceholder",
                    )}
                  />
                  {errors.addressDetails && (
                    <p className="text-xs text-destructive">
                      {t(`checkout.${errors.addressDetails.message}`)}
                    </p>
                  )}
                </div>

                {/* Landmark */}
                <div className="space-y-2">
                  <Label htmlFor="landmark">
                    {t("checkout.form.landmark")}
                  </Label>
                  <Input
                    id="landmark"
                    {...register("landmark")}
                    placeholder={t(
                      "checkout.form.landmarkPlaceholder",
                    )}
                  />
                </div>

                {/* Notes */}
                <div className="space-y-2">
                  <Label htmlFor="notes">
                    {t("checkout.form.notes")}
                  </Label>
                  <Input
                    id="notes"
                    {...register("notes")}
                    placeholder={t(
                      "checkout.form.notesPlaceholder",
                    )}
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Order Summary */}
          <div>
            <Card className="sticky top-20">
              <CardHeader>
                <CardTitle className="font-heading text-lg">
                  {t("cart.orderSummary")}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {items.map((item) => (
                  <div
                    key={item.product.id}
                    className="flex items-center gap-3"
                  >
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded bg-muted">
                      <Laptop className="h-4 w-4 text-muted-foreground/40" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-xs font-medium">
                        {item.product.name[locale]}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        × {item.quantity}
                      </p>
                    </div>
                    <span className="text-xs font-semibold">
                      {formatPrice(
                        item.product.priceEGP * item.quantity,
                      )}
                    </span>
                  </div>
                ))}
                <Separator />
                <div className="flex justify-between">
                  <span className="font-semibold">
                    {t("common.total")}
                  </span>
                  <span className="text-lg font-bold text-primary">
                    {formatPrice(getTotal())} {t("common.egp")}
                  </span>
                </div>
                <Button
                  type="submit"
                  className="w-full"
                  size="lg"
                  disabled={isSubmitting}
                >
                  {t("checkout.placeOrder")}
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </form>
    </div>
  );
}
