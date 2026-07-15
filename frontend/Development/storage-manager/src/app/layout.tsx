'use server'
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from '@/Providers/index'
import { Header } from '@/components/custom/header'
import { Footer } from '@/components/custom/footer'
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/custom/sidebar/index"
import { Toaster } from '@/components/ui/sonner';
import { cookies } from "next/headers";
import { user } from '@/Interfaces/index'


const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
});

export async function generateMetadata(): Promise<Metadata> {
    return {
        title: "Storage Manager",
        description: "Created by kaique",
    };
}

export default async function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    const user_name = (await cookies()).get('Name')?.value || ''
    let user: user | undefined = undefined
    user = { name: user_name }
    // não podemos utilizar os providers para não expor informações do usuário, alterar isso depois
    return (
        <html lang="en">
            <body
                className={`${geistSans.variable} ${geistMono.variable} antialiased w-full h-full`}
            >
                <Toaster className='w-full' position='top-center'></Toaster>
                <AuthProvider user={user}>
                    <SidebarProvider defaultOpen={false}>
                        <AppSidebar />
                        <div className="w-full flex flex-col min-h-screen bg-gray-50 justify-between">
                            <Header menuButton={<SidebarTrigger className="text-white hover:bg-[#005FB8] hover:opacity-80 hover:text-white" />}></Header>
                            <div className="w-full h-full flex justify-center content-center bg-linear-to-b from-[#003B73] to-[#005FB8]">
                                <div className='grow container px-4 py-8 justify-center content-center'>
                                    {children}
                                </div>
                            </div>
                            <Footer></Footer>
                        </div>
                    </SidebarProvider>
                </AuthProvider>
            </body>
        </html>
    );
}

