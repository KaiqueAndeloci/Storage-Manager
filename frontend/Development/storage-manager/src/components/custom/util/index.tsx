
import { fieldModel } from "@/Interfaces"
import { Label } from '@/components/ui/label';
import { Input } from "@/components/ui/input";
import { RadioButton } from "@/components/custom/input/radioButton/index"
import { InputPassword } from "@/components/custom/input/password"
import { TransferList } from "@/components/custom/input/dual-listbox/index"


export function RenderFields(
    {
        fields,
    }: {
        fields: fieldModel[],
    }
) {


    return fields.map(
        (item, index) => (
            <div key={index}>
                {
                    (() => {
                        switch (item.type) {
                            case "text":
                                return (
                                    <div className="grid gap-3" hidden={item.hidden}>
                                        <Label>{item.placeholder}</Label>
                                        <Input
                                            className={item.className}
                                            maxLength={item.maxLength}
                                            name={item.name} type="text"
                                            placeholder={item.placeholder}
                                            defaultValue={item.defaultValue}
                                        />
                                    </div>
                                );
                            case "password":
                                return (
                                    <InputPassword classNameDiv="grid gap-3" classNameInput={item.className} />
                                );
                            case "radio":
                                return (
                                    <RadioButton
                                        name={item.name}
                                        label={item.label ? item.label : []}
                                        getChecked={item.setRadioState}
                                        optionChecked={item.radioState}
                                    ></RadioButton>
                                );
                            case "dual-listbox":
                                if (item.transferListProps) {
                                    return (
                                        <TransferList available={item.transferListProps.available} selected={item.transferListProps.selected}></TransferList>
                                    );
                                } else {
                                    return (
                                        <div></div>
                                    );
                                }
                            case "email":
                                return (
                                    <div className="grid gap-3" hidden={item.hidden}>
                                        <Label>{item.placeholder}</Label>
                                        <Input
                                            className={item.className}
                                            maxLength={item.maxLength}
                                            name={item.name}
                                            type="email"
                                            placeholder={item.placeholder}
                                            defaultValue={item.defaultValue}
                                        />
                                    </div>
                                )
                            default:
                                return (
                                    <div className="grid gap-3" hidden={item.hidden}>
                                        <Label>{item.placeholder}</Label>
                                        <Input
                                            className={item.className}
                                            maxLength={item.maxLength}
                                            name={item.name}
                                            type={item.type}
                                            placeholder={item.placeholder}
                                            defaultValue={item.defaultValue}
                                        />
                                    </div>
                                );
                        }
                    })()
                }
            </div>
        )
    )
}

