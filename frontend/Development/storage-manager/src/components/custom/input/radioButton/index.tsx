import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"


// export function RadioGroupDemo({ label = [''], getChecked, isRequired, optionChecked }: { label: string[], getChecked?: (value: string) => void, isRequired?: boolean, optionChecked?: string }) {

//     return (
//         <RadioGroup required={isRequired} value="" className="self-start w-full" onValueChange={getChecked} defaultValue="comfortable">
//             {label.map((option, idx) => (
//                 <div key={idx} className="ml-5 flex items-center space-x-2">
//                     <RadioGroupItem
//onClick={}
//defaultValue={optionChecked === option ? true : false}
//defaultChecked={optionChecked === option ? true : false}
// checked={optionChecked === option ? true : false} 
//                         className="bg-white border-neutral-600" value={option} id={`option-${idx}`} />
//                     <Label htmlFor={`option-${idx}`}>{option}</Label>
//                 </div>
//             ))}
//         </RadioGroup>
//     )
// }

export function RadioButton({
    label = [''],
    name,
    getChecked,
    isRequired,
    optionChecked,
}: {
    label: string[],
    name: string,
    getChecked?: (value: string) => void,
    isRequired?: boolean,
    optionChecked?: string
}) {
    return (
        <RadioGroup
            required={isRequired}
            name={name}
            value={optionChecked ? `${optionChecked}` : undefined}
            onValueChange={getChecked}
            className="self-start w-full"
        >
            {label.map((option, idx) => (
                <div key={idx} className="flex items-center gap-3 space-x-2">
                    <RadioGroupItem
                        value={option}
                        id={`option-${idx}`}
                    />
                    <Label htmlFor={`option-${idx}`}>{option}</Label>
                </div>
            ))}
        </RadioGroup>
    )
}