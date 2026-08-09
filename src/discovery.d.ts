// Type declarations for src/discovery.mjs — the publication-boundary module.
//
// Written as a sibling .d.ts rather than by converting discovery.mjs to
// TypeScript: docusaurus.config.mjs imports the .mjs at config time, so the
// runtime module stays plain JS (ruling 14 — progressive adoption, no mass
// conversion) while callers still get a checked contract.
//
// Part of Slice A · A4 (single site configuration and TypeScript test seam).

/** One tracked MDX the deny policy rejected, with the reason it was rejected. */
export interface DeniedMdx {
  /** Repository-relative POSIX path. */
  path: string;
  /** Human-readable reason, e.g. `denied path segment: sources`. */
  reason: string;
}

/** The discovery result consumed by docusaurus.config.mjs. */
export interface SiteDiscovery {
  /** Top-level content directories, sorted. Each becomes a sidebar category. */
  bookDirs: string[];
  /** Docusaurus `include` globs, one per book dir, sorted. */
  include: string[];
  /** Per-file `exclude` globs for every non-publishable MDX, sorted. */
  exclude: string[];
  /** Count of tracked `.mdx` (`git ls-files`), before the deny policy. */
  trackedCount: number;
  /** Count that survived the deny policy. This is the published set. */
  publishableCount: number;
  /** Count rejected by the deny policy. */
  deniedCount: number;
  /** The rejected entries with reasons, sorted by path. */
  denied: DeniedMdx[];
  /** Count of on-disk MDX that is not publishable (gitignored + denied). */
  ignoredCount: number;
}

/** Non-content top-level directories kept out of the sidebar. */
export declare const DEFAULT_SKIP_DIRS: Set<string>;

/** Path segments that are never publishable, at any depth. */
export declare const DENY_SEGMENTS: Set<string>;

/** Filename stem suffixes that withhold publication (`.draft`, `.private`, …). */
export declare const DENY_FILENAME_SUFFIXES: string[];

/** Returns the offending segment, or null when no segment is denied. */
export declare function deniedBySegment(relPath: string): string | null;

/** Returns the offending filename suffix, or null. */
export declare function deniedByFilename(relPath: string): string | null;

/** Returns a reason when the path is arbitrary root MDX, else null. */
export declare function deniedAsRootMdx(relPath: string): string | null;

/**
 * Inspects only the leading front-matter block, within a bounded prefix.
 * Returns the offending `key: value`, or null when publication is not withheld.
 */
export declare function frontmatterDenial(text: string): string | null;

/**
 * Classifies one candidate. Returns null when publishable, else the reason.
 * Fail-closed: an unreadable candidate is denied, never silently published.
 */
export declare function denialReason(
  relPath: string,
  cwd?: string,
  skipDirs?: Set<string>,
): string | null;

/** Every tracked `.mdx`, before the deny policy. */
export declare function discoverTrackedMdx(cwd?: string): string[];

/** Tracked `.mdx` that survives the deny policy, sorted. */
export declare function discoverPublishableMdx(
  cwd?: string,
  skipDirs?: Set<string>,
): string[];

/** Tracked `.mdx` the deny policy rejected, with reasons, sorted by path. */
export declare function discoverDeniedMdx(
  cwd?: string,
  skipDirs?: Set<string>,
): DeniedMdx[];

/** On-disk `.mdx` that is not publishable, so Docusaurus can exclude it. */
export declare function discoverIgnoredMdx(
  cwd?: string,
  skipDirs?: Set<string>,
): string[];

/** Top-level content directories derived from a publishable set, sorted. */
export declare function discoverBookDirs(
  publishableMdx: string[],
  skipDirs?: Set<string>,
): string[];

/** Escapes each path for fast-glob/picomatch and sorts the result. */
export declare function discoverExcludePatterns(ignoredMdx: string[]): string[];

/** The full discovery result for docusaurus.config.mjs. */
export declare function discoverSite(
  cwd?: string,
  skipDirs?: Set<string>,
): SiteDiscovery;
