export class Block {
    id: number;
    name: string;
    displayName: string;
    hardness: number;
    resistance: number;
    stackSize: number;
    diggable: boolean;
    material: string;
    transparent: boolean;
    emitLight: number;
    filterLight: number;
    defaultState: number;
    minStateId: number;
    maxStateId: number;
    states: any[];
    harvestTools?: { [key: string]: boolean; };
    drops: number[];
    boundingBox: string;

    constructor(data: Partial<Block>) {
        this.id = data.id ?? 0;
        this.name = data.name ?? '';
        this.displayName = data.displayName ?? '';
        this.hardness = data.hardness ?? 0.0;
        this.resistance = data.resistance ?? 0.0;
        this.stackSize = data.stackSize ?? 64;
        this.diggable = data.diggable ?? false;
        this.material = data.material ?? 'default';
        this.transparent = data.transparent ?? false;
        this.emitLight = data.emitLight ?? 0;
        this.filterLight = data.filterLight ?? 0;
        this.defaultState = data.defaultState ?? 0;
        this.minStateId = data.minStateId ?? 0;
        this.maxStateId = data.maxStateId ?? 0;
        this.states = data.states ?? [];
        this.harvestTools = data.harvestTools ?? {};
        this.drops = data.drops ?? [];
        this.boundingBox = data.boundingBox ?? 'empty';
    }
}
