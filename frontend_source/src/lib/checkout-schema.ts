import { z } from "zod";

export const checkoutSchema = z.object({
  fullName: z
    .string()
    .min(3, "validation.nameMin")
    .max(100),
  phone: z
    .string()
    .regex(
      /^01[0125]\d{8}$/,
      "validation.phoneInvalid",
    ),
  assiutCenter: z
    .string()
    .min(1, "validation.centerRequired"),
  addressDetails: z
    .string()
    .min(10, "validation.addressMin")
    .max(500),
  landmark: z.string().optional(),
  notes: z.string().optional(),
});

export type CheckoutFormValues = z.infer<typeof checkoutSchema>;
