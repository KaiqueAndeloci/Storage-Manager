'use client'
import { useSearchParams } from 'next/navigation'
import { SidebarTrigger } from "@/components/ui/sidebar"
import routes from '@/app/routes'
import { useAuth } from '@/Providers'

export function MenuButton() {
    const authenticated = useAuth()
    const params = useSearchParams()
    const from = params.get('redirect') || routes.dashboard

    if (authenticated.user_details) {
        return (
            <div className={`h-full justify-center content-center `}>
                <SidebarTrigger className="text-white hover:bg-[#005FB8] hover:opacity-80 hover:text-white" />
            </div>
        )
    }

    return (
        <div></div>
    )
}