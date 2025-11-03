'use server'
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from '@/providers/index'
import { Header } from '@/components/custom/header'
import { Footer } from '@/components/custom/footer'
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/custom/sidebar/index"
import { Toaster } from '@/components/ui/sonner';
import { cookies } from "next/headers";
import { user } from '@/interfaces/index'


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
    const user_name = (await cookies()).get('user_name')?.value || ''
    const user_email = (await cookies()).get('user_email')?.value || ''
    const user_permission = (await cookies()).get('user_permission')?.value || ''
    const date_creation = (await cookies()).get('date_creation')?.value || ''
    let user: user | undefined = undefined
    if (user_permission === 'ADMIN' || user_permission === 'cashier' || user_permission === 'logistic') {
        user = { name: user_name, email: user_email, date_creation: date_creation, permission_type: user_permission }
    }
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
                            <div className="w-full h-full flex justify-center content-center bg-gradient-to-b from-[#003B73] to-[#005FB8]">
                                <div className='flex-grow container px-4 py-8 justify-center content-center'>
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

