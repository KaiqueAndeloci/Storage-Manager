'use client'
import { Button } from "@/components/ui/button"
import { Spinner } from '@/components/ui/spinner';
import {
    Sheet,
    SheetClose,
    SheetContent,
    SheetDescription,
    SheetFooter,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from "@/components/ui/sheet"

export function SheetDemo({ title, hiddenButton, titleButton, children, loadingUser, openStatus, onOpenChange, handleOnClick }:
    {
        title: string,
        hiddenButton: boolean,
        titleButton: string,
        children: React.ReactNode,
        loadingUser: boolean,
        openStatus: boolean,
        onOpenChange: (open: boolean) => void,
        handleOnClick?: () => void
    }) {

    return (
        <Sheet
            open={openStatus}
            onOpenChange={onOpenChange}
        >
            <SheetTrigger asChild >
                <Button onClick={handleOnClick} hidden={hiddenButton} variant="outline">{titleButton}</Button>
            </SheetTrigger>
            <SheetContent>
                <SheetHeader>
                    <SheetTitle>{title}</SheetTitle>
                </SheetHeader>

                {loadingUser ? (
                    <div className="flex h-full items-center justify-center">
                        <Spinner />
                        <span>Carregando...</span>
                    </div>
                ) : (
                    <>
                        {children}
                    </>
                )}

            </SheetContent>
        </Sheet>
    )
}
