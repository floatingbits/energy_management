import type { TimeSeries } from "./forecast";

/**
 * Semaphore decoding of raw API time series payloads.
 *
 * This is the single frontend location that knows what
 * `value_type_definition` payloads on the wire mean. Everything
 * downstream (charts etc.) consumes the semantic DecodedSeries
 * types defined here, so consumers never parse raw value arrays
 * themselves.
 */
export interface SlotValues {
    slotIndex: number;
    values: (number | null)[];
}

/** Quantile series: levels are percents, indexed equal to each value's payload slot. */
export interface QuantileSeries {
    kind: "quantile";
    /** Percent levels, ascending and aligned to the slot values, e.g. [5, 50, 95]. */
    quantiles: number[];
    /** Series-name level label, e.g. 5 -> "p05". */
    labelFor: (index: number) => string;
    slots: SlotValues[];
}

/** Scalar series: exactly one value per slot. */
export interface ScalarSeries {
    kind: "scalar";
    slots: { slotIndex: number; value: number }[];
}

export type DecodedSeries = QuantileSeries | ScalarSeries;

/** Label for a quantile level in percent: 5 -> "p05", 50 -> "p50", 2.5 -> "p2.5". */
export function quantileLabel(level: number): string {
    return `p${String(level).padStart(2, "0")}`;
}

export function decodeSeries(series: TimeSeries): DecodedSeries {
    const definition = JSON.parse(series.value_type_definition);

    switch (definition.type) {
        case "quantile": {
            const quantiles = definition.quantiles as number[];
            return {
                kind: "quantile",
                quantiles,
                labelFor: (index: number) => quantileLabel(quantiles[index]),
                slots: series.values.map(value => ({
                    slotIndex: value.slot_index,
                    values: value.values,
                })),
            };
        }
        case "scalar":
            return {
                kind: "scalar",
                slots: series.values.map(value => {
                    if (value.values.length < 1 || value.values[0] === null) {
                        throw new Error(
                            `Scalar series ${series.metric} has empty slot ${value.slot_index}`
                        );
                    }
                    return { slotIndex: value.slot_index, value: value.values[0] };
                }),
            };
        default:
            throw new Error(
                `Unknown value_type_definition for series ${series.metric}: ${series.value_type_definition}`
            );
    }
}
