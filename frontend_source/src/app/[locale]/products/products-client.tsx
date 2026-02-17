"use client";

import { useState, useMemo } from "react";
import { useTranslations, useLocale } from "next-intl";
import { useSearchParams } from "next/navigation";
import { products, brands, ramOptions, cpuFamilies, screenSizes } from "@/data/products";
import { Product } from "@/types/product";
import { ProductGrid } from "@/components/product-grid";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
import { SlidersHorizontal, X } from "lucide-react";

const ITEMS_PER_PAGE = 12;

type SortOption = "newest" | "priceLow" | "priceHigh";

interface Filters {
  brands: string[];
  ram: string[];
  cpu: string[];
  screen: string[];
  inStockOnly: boolean;
  includesCharger: boolean;
  gpuDedicated: boolean;
  grades: string[];
  keyboard: string[];
  priceMin: number;
  priceMax: number;
}

const defaultFilters: Filters = {
  brands: [],
  ram: [],
  cpu: [],
  screen: [],
  inStockOnly: false,
  includesCharger: false,
  gpuDedicated: false,
  grades: [],
  keyboard: [],
  priceMin: 0,
  priceMax: 50000,
};

export function ProductsClient() {
  const t = useTranslations();
  const locale = useLocale() as "ar" | "en";
  const searchParams = useSearchParams();
  const brandParam = searchParams.get("brand");

  const [filters, setFilters] = useState<Filters>({
    ...defaultFilters,
    brands: brandParam ? [brandParam] : [],
  });
  const [sort, setSort] = useState<SortOption>("newest");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    let result = [...products];

    if (filters.brands.length > 0) {
      result = result.filter((p) =>
        filters.brands.includes(p.brand),
      );
    }
    if (filters.ram.length > 0) {
      result = result.filter((p) =>
        filters.ram.some((r) => p.specs.ram.includes(r)),
      );
    }
    if (filters.cpu.length > 0) {
      result = result.filter((p) =>
        filters.cpu.some((c) =>
          p.specs.cpu.toLowerCase().includes(c.toLowerCase()),
        ),
      );
    }
    if (filters.screen.length > 0) {
      result = result.filter((p) =>
        filters.screen.some((s) => p.specs.screen.includes(s)),
      );
    }
    if (filters.inStockOnly) {
      result = result.filter((p) => p.inStock);
    }
    if (filters.includesCharger) {
      result = result.filter((p) => p.includesCharger);
    }
    if (filters.gpuDedicated) {
      result = result.filter(
        (p) =>
          p.specs.gpu.toLowerCase().includes("nvidia") ||
          p.specs.gpu.toLowerCase().includes("radeon") ||
          p.specs.gpu.toLowerCase().includes("geforce"),
      );
    }
    if (filters.grades.length > 0) {
      result = result.filter((p) =>
        filters.grades.includes(p.grade),
      );
    }
    if (filters.keyboard.length > 0) {
      result = result.filter((p) =>
        filters.keyboard.includes(p.keyboardLayout),
      );
    }
    result = result.filter(
      (p) =>
        p.priceEGP >= filters.priceMin &&
        p.priceEGP <= filters.priceMax,
    );

    switch (sort) {
      case "priceLow":
        result.sort((a, b) => a.priceEGP - b.priceEGP);
        break;
      case "priceHigh":
        result.sort((a, b) => b.priceEGP - a.priceEGP);
        break;
      default:
        break;
    }

    return result;
  }, [filters, sort]);

  const paginated = filtered.slice(0, page * ITEMS_PER_PAGE);
  const hasMore = paginated.length < filtered.length;

  const activeFilterCount =
    filters.brands.length +
    filters.ram.length +
    filters.cpu.length +
    filters.screen.length +
    filters.grades.length +
    filters.keyboard.length +
    (filters.inStockOnly ? 1 : 0) +
    (filters.includesCharger ? 1 : 0) +
    (filters.gpuDedicated ? 1 : 0);

  const clearFilters = () => {
    setFilters(defaultFilters);
    setPage(1);
  };

  const toggleArrayFilter = (
    key: keyof Filters,
    value: string,
  ) => {
    setFilters((prev) => {
      const arr = prev[key] as string[];
      const next = arr.includes(value)
        ? arr.filter((v) => v !== value)
        : [...arr, value];
      return { ...prev, [key]: next };
    });
    setPage(1);
  };

  const FilterPanel = () => (
    <div className="space-y-6">
      {/* Brand */}
      <div>
        <h4 className="mb-3 text-sm font-semibold">
          {t("products.filters.brand")}
        </h4>
        <div className="space-y-2">
          {brands.map((brand) => (
            <label
              key={brand}
              className="flex cursor-pointer items-center gap-2"
            >
              <Checkbox
                checked={filters.brands.includes(brand)}
                onCheckedChange={() =>
                  toggleArrayFilter("brands", brand)
                }
              />
              <span className="text-sm">{brand}</span>
            </label>
          ))}
        </div>
      </div>

      <Separator />

      {/* RAM */}
      <div>
        <h4 className="mb-3 text-sm font-semibold">
          {t("products.filters.ram")}
        </h4>
        <div className="space-y-2">
          {ramOptions.map((ram) => (
            <label
              key={ram}
              className="flex cursor-pointer items-center gap-2"
            >
              <Checkbox
                checked={filters.ram.includes(ram)}
                onCheckedChange={() =>
                  toggleArrayFilter("ram", ram)
                }
              />
              <span className="text-sm">{ram}</span>
            </label>
          ))}
        </div>
      </div>

      <Separator />

      {/* CPU */}
      <div>
        <h4 className="mb-3 text-sm font-semibold">
          {t("products.filters.cpu")}
        </h4>
        <div className="space-y-2">
          {cpuFamilies.map((cpu) => (
            <label
              key={cpu}
              className="flex cursor-pointer items-center gap-2"
            >
              <Checkbox
                checked={filters.cpu.includes(cpu)}
                onCheckedChange={() =>
                  toggleArrayFilter("cpu", cpu)
                }
              />
              <span className="text-sm">{cpu}</span>
            </label>
          ))}
        </div>
      </div>

      <Separator />

      {/* Screen */}
      <div>
        <h4 className="mb-3 text-sm font-semibold">
          {t("products.filters.screenSize")}
        </h4>
        <div className="space-y-2">
          {screenSizes.map((size) => (
            <label
              key={size}
              className="flex cursor-pointer items-center gap-2"
            >
              <Checkbox
                checked={filters.screen.includes(size)}
                onCheckedChange={() =>
                  toggleArrayFilter("screen", size)
                }
              />
              <span className="text-sm">{size}</span>
            </label>
          ))}
        </div>
      </div>

      <Separator />

      {/* Grade */}
      <div>
        <h4 className="mb-3 text-sm font-semibold">
          {t("products.filters.grade")}
        </h4>
        <div className="space-y-2">
          {["A", "B", "C"].map((grade) => (
            <label
              key={grade}
              className="flex cursor-pointer items-center gap-2"
            >
              <Checkbox
                checked={filters.grades.includes(grade)}
                onCheckedChange={() =>
                  toggleArrayFilter("grades", grade)
                }
              />
              <span className="text-sm">{t("common.grade")} {grade}</span>
            </label>
          ))}
        </div>
      </div>

      <Separator />

      {/* Keyboard */}
      <div>
        <h4 className="mb-3 text-sm font-semibold">
          {t("products.filters.keyboard")}
        </h4>
        <div className="space-y-2">
          {(["EN", "AR", "AR-EN", "Unknown"] as const).map((kb) => (
            <label
              key={kb}
              className="flex cursor-pointer items-center gap-2"
            >
              <Checkbox
                checked={filters.keyboard.includes(kb)}
                onCheckedChange={() =>
                  toggleArrayFilter("keyboard", kb)
                }
              />
              <span className="text-sm">
                {t(`keyboardLayouts.${kb}`)}
              </span>
            </label>
          ))}
        </div>
      </div>

      <Separator />

      {/* Toggles */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Label className="text-sm">
            {t("products.filters.inStockOnly")}
          </Label>
          <Switch
            checked={filters.inStockOnly}
            onCheckedChange={(v) => {
              setFilters((prev) => ({
                ...prev,
                inStockOnly: v,
              }));
              setPage(1);
            }}
          />
        </div>
        <div className="flex items-center justify-between">
          <Label className="text-sm">
            {t("products.filters.charger")}
          </Label>
          <Switch
            checked={filters.includesCharger}
            onCheckedChange={(v) => {
              setFilters((prev) => ({
                ...prev,
                includesCharger: v,
              }));
              setPage(1);
            }}
          />
        </div>
        <div className="flex items-center justify-between">
          <Label className="text-sm">
            {t("products.filters.dedicated")} {t("products.filters.gpu")}
          </Label>
          <Switch
            checked={filters.gpuDedicated}
            onCheckedChange={(v) => {
              setFilters((prev) => ({
                ...prev,
                gpuDedicated: v,
              }));
              setPage(1);
            }}
          />
        </div>
      </div>
    </div>
  );

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="font-heading text-2xl font-bold sm:text-3xl">
          {t("products.title")}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {t("products.subtitle")}
        </p>
      </div>

      {/* Top bar: result count + sort + mobile filter */}
      <div className="mb-6 flex flex-wrap items-center gap-3">
        <p className="text-sm text-muted-foreground">
          {t("products.showing")}{" "}
          <strong>{paginated.length}</strong>{" "}
          {t("products.of")}{" "}
          <strong>{filtered.length}</strong>{" "}
          {t("products.laptops")}
        </p>

        <div className="flex-1" />

        {/* Sort */}
        <Select
          value={sort}
          onValueChange={(v) => setSort(v as SortOption)}
        >
          <SelectTrigger className="w-44">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="newest">
              {t("products.sort.newest")}
            </SelectItem>
            <SelectItem value="priceLow">
              {t("products.sort.priceLow")}
            </SelectItem>
            <SelectItem value="priceHigh">
              {t("products.sort.priceHigh")}
            </SelectItem>
          </SelectContent>
        </Select>

        {/* Mobile filter button */}
        <Sheet>
          <SheetTrigger asChild>
            <Button
              variant="outline"
              size="sm"
              className="gap-2 lg:hidden"
            >
              <SlidersHorizontal className="h-4 w-4" />
              {t("common.filters")}
              {activeFilterCount > 0 && (
                <Badge className="ml-1 h-5 w-5 rounded-full p-0 text-[10px]">
                  {activeFilterCount}
                </Badge>
              )}
            </Button>
          </SheetTrigger>
          <SheetContent side={locale === "ar" ? "right" : "left"} className="w-80 overflow-y-auto">
            <SheetHeader>
              <SheetTitle>{t("common.filters")}</SheetTitle>
            </SheetHeader>
            <div className="mt-6">
              <FilterPanel />
            </div>
          </SheetContent>
        </Sheet>
      </div>

      {/* Active filter chips */}
      {activeFilterCount > 0 && (
        <div className="mb-4 flex flex-wrap items-center gap-2">
          {filters.brands.map((b) => (
            <Badge
              key={b}
              variant="secondary"
              className="cursor-pointer gap-1"
              onClick={() => toggleArrayFilter("brands", b)}
            >
              {b}
              <X className="h-3 w-3" />
            </Badge>
          ))}
          {filters.ram.map((r) => (
            <Badge
              key={r}
              variant="secondary"
              className="cursor-pointer gap-1"
              onClick={() => toggleArrayFilter("ram", r)}
            >
              {r}
              <X className="h-3 w-3" />
            </Badge>
          ))}
          {filters.cpu.map((c) => (
            <Badge
              key={c}
              variant="secondary"
              className="cursor-pointer gap-1"
              onClick={() => toggleArrayFilter("cpu", c)}
            >
              {c}
              <X className="h-3 w-3" />
            </Badge>
          ))}
          <Button
            variant="ghost"
            size="sm"
            onClick={clearFilters}
            className="text-xs text-destructive"
          >
            {t("common.clearAll")}
          </Button>
        </div>
      )}

      {/* Layout: sidebar + grid */}
      <div className="flex gap-8">
        {/* Desktop sidebar */}
        <aside className="hidden w-56 shrink-0 lg:block">
          <div className="sticky top-20">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-heading text-sm font-bold">
                {t("common.filters")}
              </h3>
              {activeFilterCount > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearFilters}
                  className="h-auto p-0 text-xs text-destructive"
                >
                  {t("common.clearAll")}
                </Button>
              )}
            </div>
            <FilterPanel />
          </div>
        </aside>

        {/* Grid */}
        <div className="min-w-0 flex-1">
          {filtered.length === 0 ? (
            <div className="py-16 text-center">
              <p className="text-muted-foreground">
                {t("common.noResults")}
              </p>
              <Button
                variant="link"
                onClick={clearFilters}
                className="mt-2"
              >
                {t("common.clearAll")}
              </Button>
            </div>
          ) : (
            <>
              <ProductGrid products={paginated} />
              {hasMore && (
                <div className="mt-8 text-center">
                  <Button
                    variant="outline"
                    onClick={() => setPage((p) => p + 1)}
                  >
                    {t("common.loadMore")}
                  </Button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
