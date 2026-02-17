export type Condition = "imported-used" | "imported-refurbished" | "used";
export type Grade = "A" | "B" | "C";
export type KeyboardLayout = "AR" | "EN" | "AR-EN" | "Unknown";

export interface Product {
  id: string;
  slug: string;
  name: { ar: string; en: string };
  brand: string;
  priceEGP: number;
  oldPriceEGP?: number;
  images: string[];
  inStock: boolean;
  condition: Condition;
  grade: Grade;
  includesCharger: boolean;
  keyboardLayout: KeyboardLayout;
  shortSpecs: { ar: string[]; en: string[] };
  specs: {
    cpu: string;
    ram: string;
    storage: string;
    gpu: string;
    screen: string;
    battery: string;
    warranty: string;
  };
  tags?: string[];
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface CheckoutFormData {
  fullName: string;
  phone: string;
  assiutCenter: string;
  addressDetails: string;
  landmark?: string;
  notes?: string;
}
