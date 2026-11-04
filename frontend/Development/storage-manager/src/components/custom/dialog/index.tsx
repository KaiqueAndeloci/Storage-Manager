import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"

export function DialogDemo({ title, children }: { title: string, children: React.ReactNode }) {
    return (
        <Dialog>
            <DialogTrigger asChild><Button className="hover:cursor-pointer" variant="outline">No Close Button</Button></DialogTrigger>
            <DialogContent className="flex" showCloseButton={false}>
                <DialogHeader className="flex">
                    <DialogTitle>{title}</DialogTitle>
                    {children}
                </DialogHeader>
                <DialogFooter>
                    <DialogClose className="hover:cursor-pointer">Close</DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
