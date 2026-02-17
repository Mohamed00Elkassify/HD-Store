"use client";

import { Product } from "@/types/product";
import { useTranslations, useLocale } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useCartStore } from "@/store/cart";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { ShoppingCart } from "lucide-react";
import { ProductImage } from "./product-image";
import { formatPrice } from "@/lib/constants";
import { toast } from "sonner";

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  const t = useTranslations();
  const locale = useLocale() as "ar" | "en";
  const addItem = useCartStore((s) => s.addItem);

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    addItem(product);
    toast.success(t("cart.itemAdded"));
  };

  return (
    <Card className="group relative overflow-hidden transition-all hover:shadow-lg">
      {/* Tags */}
      {product.tags && product.tags.length > 0 && (
        <div className="absolute left-2 top-2 z-10 flex flex-col gap-1 rtl:left-auto rtl:right-2">
          {product.tags.map((tag) => (
            <Badge
              key={tag}
              className="bg-primary text-xs text-primary-foreground"
            >
              {tag}
            </Badge>
          ))}
        </div>
      )}

      {/* Out of stock overlay */}
      {!product.inStock && (
        <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/80">
          <Badge variant="destructive" className="text-sm">
            {t("common.outOfStock")}
          </Badge>
        </div>
      )}

      <Link href={`/products/${product.slug}`}>
        <div className="relative aspect-[4/3] w-full overflow-hidden">
          <ProductImage
            src={product.images?.[0]}
            alt={product.name[locale]}
            className="aspect-[4/3] transition-transform group-hover:scale-105"
            fill
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          />
        </div>

        <CardContent className="space-y-3 p-4">
          {/* Brand + Grade */}
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-muted-foreground">
              {product.brand}
            </span>
            <Badge variant="secondary" className="text-xs">
              {t("common.grade")} {product.grade}
            </Badge>
          </div>

          {/* Name */}
          <h3 className="line-clamp-2 text-sm font-semibold leading-tight">
            {product.name[locale]}
          </h3>

          {/* Short Specs (2 lines max) */}
          <div className="space-y-0.5">
            {product.shortSpecs[locale].map((spec, i) => (
              <p
                key={i}
                className="line-clamp-1 text-xs text-muted-foreground"
              >
                {spec}
              </p>
            ))}
          </div>

          {/* Price */}
          <div className="flex items-baseline gap-2">
            <span className="text-lg font-bold text-primary">
              {formatPrice(product.priceEGP)}
            </span>
            <span className="text-xs text-muted-foreground">
              {t("common.egp")}
            </span>
            {product.oldPriceEGP && (
              <span className="text-xs text-muted-foreground line-through">
                {formatPrice(product.oldPriceEGP)}
              </span>
            )}
          </div>

          {/* CTA */}
          <Button
            size="sm"
            className="w-full gap-2"
            onClick={handleAddToCart}
            disabled={!product.inStock}
          >
            <ShoppingCart className="h-3.5 w-3.5" />
            {t("common.orderNow")}
          </Button>
        </CardContent>
      </Link>
    </Card>
  );
}

export function ProductCardSkeleton() {
  return (
    <Card className="overflow-hidden">
      <div className="aspect-[4/3] animate-pulse bg-muted" />
      <CardContent className="space-y-3 p-4">
        <div className="flex justify-between">
          <div className="h-3 w-12 animate-pulse rounded bg-muted" />
          <div className="h-5 w-16 animate-pulse rounded bg-muted" />
        </div>
        <div className="h-4 w-full animate-pulse rounded bg-muted" />
        <div className="h-3 w-3/4 animate-pulse rounded bg-muted" />
        <div className="h-3 w-2/3 animate-pulse rounded bg-muted" />
        <div className="h-6 w-24 animate-pulse rounded bg-muted" />
        <div className="h-9 w-full animate-pulse rounded bg-muted" />
      </CardContent>
    </Card>
  );
}
