'use client'
import { CircleX } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import { AuthenticateContext, message_type } from "@/interfaces/index"


export function Notify({ message, message_type }: { message: string, message_type: message_type }) {
    function notification(message: string, error: boolean) {
        toast.custom(
            (t) => (
                <div className={cn('w-full border-b-blue-300 p-4 rounded-lg shadow-lg', error ? 'text-red-600 bg-red-200' : 'text-white bg-black')}>
                    <div className="flex justify-between items-center gap-2">
                        <div>
                            <div className="font-semibold">Notify</div>
                            <div className={"text-sm opacity-90"}>{`${message}`}</div>
                        </div>
                        <Button
                            onClick={() => toast.dismiss(t)}
                            className={cn("size-10", 'px-2 py-1 text-xs', error ? 'bg-black/20 hover:bg-black/30 text-black' : 'bg-white/20 hover:bg-white/30')}
                            size="icon"
                        >
                            <CircleX></CircleX>
                        </Button>
                    </div>
                </div>
            ),
            {
                duration: Infinity,
                className: 'w-full'
            }
        )
    }


    if (message_type === 'ERROR') {
        notification(message, true)
    }
    else {
        notification(message, false)
    }
}