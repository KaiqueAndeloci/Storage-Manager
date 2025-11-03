import { Calendar, Home, Inbox, Menu, Search, Settings, ChartPie } from "lucide-react"
import routes from "@/app/routes"
import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"

type Item = {
    title: string
    url: string
    icon: typeof Home
}

// const items: Item[] = Object.entries(routes).map(
//     ([key, value]) => ({
//         title: key,
//         url: value,
//         icon: Home,
//     })
// );

const items: Item[] = [
    {
        title: "Pages",
        url: routes.pages,
        icon: Home,
    },
    {
        title: "Dashboard",
        url: routes.dashboard,
        icon: ChartPie,
    }
]

export function AppSidebar() {
    return (
        <Sidebar>
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel>Navigation Menu</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {items.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton asChild>
                                        <a href={item.url}>
                                            <item.icon />
                                            <span>{item.title}</span>
                                        </a>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    )
}