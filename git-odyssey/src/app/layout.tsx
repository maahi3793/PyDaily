import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata: Metadata = {
  title: "Git Odyssey | Learn Git Interactively",
  description: "The best Git learning platform on the internet. Master version control through interactive missions.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Enforcing dark mode by default for premium feel
  return (
    <html lang="en" className="dark scroll-smooth">
      <body className={`${inter.className} antialiased min-h-screen bg-background text-foreground`}>
        {children}
      </body>
    </html>
  );
}
