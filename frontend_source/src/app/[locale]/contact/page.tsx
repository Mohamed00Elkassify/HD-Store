import { getTranslations } from "next-intl/server";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Phone,
  MapPin,
  Clock,
  MessageCircle,
} from "lucide-react";
import {
  getWhatsAppLink,
  WHATSAPP_DISPLAY,
  WORKING_HOURS,
} from "@/lib/constants";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "contact" });
  return {
    title: `${t("title")} — HD Store`,
    description: t("subtitle"),
  };
}

export default async function ContactPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "contact" });

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center">
        <h1 className="font-heading text-3xl font-bold sm:text-4xl">
          {t("title")}
        </h1>
        <p className="mt-2 text-muted-foreground">
          {t("subtitle")}
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-3">
        {/* Phone */}
        <Card>
          <CardContent className="flex flex-col items-center gap-3 p-6 text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
              <Phone className="h-6 w-6 text-primary" />
            </div>
            <h3 className="font-heading text-sm font-bold">
              {t("phone")}
            </h3>
            <p className="text-sm text-muted-foreground" dir="ltr">
              {WHATSAPP_DISPLAY}
            </p>
          </CardContent>
        </Card>

        {/* Address */}
        <Card>
          <CardContent className="flex flex-col items-center gap-3 p-6 text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
              <MapPin className="h-6 w-6 text-primary" />
            </div>
            <h3 className="font-heading text-sm font-bold">
              {t("address")}
            </h3>
            <p className="text-sm text-muted-foreground">
              {t("addressValue")}
            </p>
          </CardContent>
        </Card>

        {/* Hours */}
        <Card>
          <CardContent className="flex flex-col items-center gap-3 p-6 text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
              <Clock className="h-6 w-6 text-primary" />
            </div>
            <h3 className="font-heading text-sm font-bold">
              {t("hours")}
            </h3>
            <p className="text-sm text-muted-foreground">
              {t("hoursValue")}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* CTAs */}
      <div className="mt-8 flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
        <a
          href={getWhatsAppLink()}
          target="_blank"
          rel="noopener noreferrer"
        >
          <Button size="lg" className="gap-2">
            <MessageCircle className="h-5 w-5" />
            {t("chatWhatsApp")}
          </Button>
        </a>
        <a href={`tel:${WHATSAPP_DISPLAY}`}>
          <Button variant="outline" size="lg" className="gap-2">
            <Phone className="h-4 w-4" />
            {t("callNow")}
          </Button>
        </a>
      </div>

      {/* Map placeholder */}
      <Card className="mt-12 overflow-hidden">
        <div className="flex h-64 items-center justify-center bg-muted">
          <div className="text-center text-muted-foreground">
            <MapPin className="mx-auto mb-2 h-8 w-8" />
            <p className="text-sm font-medium">{t("findUs")}</p>
            <p className="text-xs">
              {t("addressValue")}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
