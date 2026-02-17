export const WHATSAPP_NUMBER = "201066537666";
export const WHATSAPP_DISPLAY = "01066537666";
export const STORE_ADDRESS_AR =
  "شارع الجمهورية - أبراج عثمان - أمام بنك القاهرة، أسيوط، مصر";
export const STORE_ADDRESS_EN =
  "Al-Gomhoria St, Othman Towers - In front of Bank of Cairo, Asyut, Egypt";
export const WORKING_HOURS = "12:00 PM – 12:00 AM";
export const STORE_PHONE = "01066537666";

export function getWhatsAppLink(message?: string): string {
  const base = `https://wa.me/${WHATSAPP_NUMBER}`;
  if (message) {
    return `${base}?text=${encodeURIComponent(message)}`;
  }
  return base;
}

export function formatPrice(price: number): string {
  return price.toLocaleString("en-US");
}
