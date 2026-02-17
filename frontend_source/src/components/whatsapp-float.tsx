"use client";

import { MessageCircle } from "lucide-react";
import { getWhatsAppLink } from "@/lib/constants";
import { useTranslations } from "next-intl";

export function WhatsAppFloat() {
  const t = useTranslations("whatsapp");

  return (
    <a
      href={getWhatsAppLink()}
      target="_blank"
      rel="noopener noreferrer"
      className="fixed bottom-6 z-50 flex items-center
        gap-2 rounded-full bg-[#25D366] px-4 py-3 text-white
        shadow-lg transition-all hover:scale-105
        hover:shadow-xl ltr:right-6 rtl:left-6"
      aria-label={t("chatWithUs")}
    >
      <MessageCircle className="h-5 w-5 fill-current" />
      <span className="hidden text-sm font-semibold sm:inline">
        {t("chatWithUs")}
      </span>
    </a>
  );
}
