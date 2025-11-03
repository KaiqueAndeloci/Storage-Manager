'use server'
import { MenuButton } from "@/components/custom/menu_button"


export async function Header({ menuButton }: { menuButton: React.ReactElement }) {

    return (
        <header className="w-full h-fit bg-[#003B73]">
            <div className="h-full flex flex-row justify-start items-center gap-12">
                <MenuButton></MenuButton>

                <div className="h-fit justify-center content-center">
                    <img width={200} height={200} alt="Logo" src={'/Logo 7.png'}></img>
                </div>
            </div>
        </header>
    )
}