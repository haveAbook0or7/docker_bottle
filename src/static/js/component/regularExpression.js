const REGEX = {
    ID_REGEX: /(?!guest)^[a-zA-Z0-9]{2,40}$/,
    PASS_REGEX: /^[a-zA-Z0-9]{6,8}$/,
    EMAIL_EWGEX: /^[a-zA-Z0-9_+-]+(\.[a-zA-Z0-9_+-]+)*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/,
    FILE_NAME_REGEX: /^(?!_|-|[0-9]).*^[ぁ-んァ-ヶ一-龠_a-zA-Z0-9_-]{1,20}$.*(?<!_|-)$/,
};
function getREGEX(label){
    return REGEX[label];
}