"use client";

import { useState } from "react";
import Image from "next/image";
import { Laptop } from "lucide-react";

interface ProductImageProps {
  src: string | undefined;
  alt: string;
  className?: string;
  fill?: boolean;
  sizes?: string;
  priority?: boolean;
}

/** Renders product image with fallback to Laptop icon when missing or on error. */
export function ProductImage({
  src,
  alt,
  className,
  fill,
  sizes,
  priority,
}: ProductImageProps) {
  const [error, setError] = useState(false);

  if (!src || error) {
    return (
      <div
        className={`flex items-center justify-center bg-muted p-4 ${className ?? ""}`}
      >
        <Laptop className="h-16 w-16 text-muted-foreground/40 sm:h-32 sm:w-32" />
      </div>
    );
  }

  const isExternal = src.startsWith("http");

  if (fill) {
    return (
      <Image
        src={src}
        alt={alt}
        fill
        className={`object-cover ${className ?? ""}`}
        sizes={sizes}
        priority={priority}
        onError={() => setError(true)}
      />
    );
  }

  return (
    <div className={`relative overflow-hidden bg-muted ${className ?? ""}`}>
      <Image
        src={src}
        alt={alt}
        width={400}
        height={300}
        className="h-full w-full object-cover"
        sizes={sizes}
        priority={priority}
        onError={() => setError(true)}
      />
    </div>
  );
}
