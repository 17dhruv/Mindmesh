import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { MouseGlow } from "@/components/ui/MouseGlow";
import { AuthProvider } from "@/contexts/AuthContext";
import { Toaster } from "react-hot-toast";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Mindmesh - Organize Your Thoughts Naturally",
  description: "A hybrid note-taking and mind mapping tool with a calming handwritten sketchbook aesthetic. Combine the power of Notion-like blocks with visual mind mapping.",
  keywords: ["note-taking", "mind mapping", "organization", "planning", "handwritten", "sketchbook"],
  authors: [{ name: "Mindmesh Team" }],
  openGraph: {
    title: "Mindmesh - Organize Your Thoughts Naturally",
    description: "A calming space for your ideas with handwritten aesthetic and visual organization.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <MouseGlow />
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'rgba(10, 10, 11, 0.9)',
                color: '#fff',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
              },
              success: {
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#fff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </AuthProvider>
      </body>
    </html>
  );
}
