"use client";

import { useState, useRef, useEffect } from "react";
import { useTranslations, useLocale } from "next-intl";
import { useRouter } from "@/i18n/navigation";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import { products } from "@/data/products";

export function SearchAutosuggest() {
  const t = useTranslations("common");
  const locale = useLocale() as "ar" | "en";
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const suggestions = query.trim().length >= 2
    ? products
        .filter((p) => {
          const q = query.toLowerCase();
          return (
            p.name[locale].toLowerCase().includes(q) ||
            p.brand.toLowerCase().includes(q) ||
            p.specs.cpu.toLowerCase().includes(q) ||
            p.specs.ram.toLowerCase().includes(q)
          );
        })
        .slice(0, 5)
    : [];

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(
        `/search?q=${encodeURIComponent(query.trim())}`,
      );
      setOpen(false);
      setQuery("");
    }
  };

  return (
    <div ref={ref} className="relative">
      <form onSubmit={handleSubmit}>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground rtl:left-auto rtl:right-3" />
          <Input
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setOpen(true);
            }}
            onFocus={() => setOpen(true)}
            placeholder={t("searchPlaceholder")}
            className="h-9 pl-9 rtl:pl-3 rtl:pr-9"
          />
        </div>
      </form>

      {open && suggestions.length > 0 && (
        <div className="absolute top-full z-50 mt-1 w-full rounded-lg border bg-popover p-1 shadow-lg">
          {suggestions.map((product) => (
            <button
              key={product.id}
              className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-left text-sm hover:bg-accent rtl:text-right"
              onClick={() => {
                router.push(`/products/${product.slug}`);
                setOpen(false);
                setQuery("");
              }}
            >
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded bg-muted">
                <Search className="h-3 w-3 text-muted-foreground" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate font-medium">
                  {product.name[locale]}
                </p>
                <p className="text-xs text-muted-foreground">
                  {product.brand} — {product.priceEGP.toLocaleString()} {t("egp")}
                </p>
              </div>
            </button>
          ))}
          <button
            className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-primary hover:bg-accent"
            onClick={() => {
              router.push(
                `/search?q=${encodeURIComponent(query.trim())}`,
              );
              setOpen(false);
              setQuery("");
            }}
          >
            <Search className="h-3 w-3" />
            {t("search")} &quot;{query}&quot;
          </button>
        </div>
      )}
    </div>
  );
}
