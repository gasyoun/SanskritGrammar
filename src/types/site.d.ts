// Shared site types for the TypeScript seam (Slice A · A4).
//
// These describe contracts the site CONSUMES; they never duplicate a Python
// domain rule (architecture § 16: TypeScript consumes serialized contracts or
// generated types, it does not re-implement domain logic). The authority for
// rights values is pipelines/work.schema.json and sg_tooling.domain — the
// RightsClass union below mirrors it and must be updated with it, never
// independently of it.
//
// Adding a file to tsconfig.json's `include` is how a future slice opts into
// checking. Nothing here converts an existing .jsx component.

/**
 * Rights classes shared by the work and pipeline contracts.
 *
 * `'unknown'` is representable and is NOT permission: the publication gate
 * fails closed on anything outside {@link PublicationSafeRights}.
 */
export type RightsClass =
  | 'publishable'
  | 'publishable-derived-input'
  | 'restricted-source'
  | 'per-file'
  | 'unknown';

/** The only rights classes the publication boundary accepts. */
export type PublicationSafeRights = 'publishable' | 'publishable-derived-input';

/** A semantic stable identity, never path-derived (architecture § 6.4). */
export type StableId =
  | `work:${string}`
  | `pipeline:${string}`
  | `sangram:${string}`
  | `external:${string}`
  | `repo:${string}`;

/** Front-matter fields the discovery boundary reads. Everything else is prose. */
export interface PublicationFrontmatter {
  title?: string;
  /** `true` withholds publication. */
  draft?: boolean;
  /** `true` withholds publication. */
  private?: boolean;
  /** `true` withholds publication. */
  archived?: boolean;
  /** `false` withholds publication (inverse form). */
  publish?: boolean;
}

/** One parsed grid-table cell, as produced by src/remark/rstTableParser.mjs. */
export interface RstTableCell {
  text: string;
  rowSpan: number;
  colSpan: number;
  header: boolean;
}

/** The parser's return shape: header rows and body rows, each a cell list. */
export interface RstTableModel {
  headerRows: RstTableCell[][];
  bodyRows: RstTableCell[][];
}
