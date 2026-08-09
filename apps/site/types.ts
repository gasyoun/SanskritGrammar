export type RightsStatus = 'unknown' | 'public-domain' | 'licensed' | 'restricted';

export interface WorkProvenanceLink {
  workId: string;
  status: RightsStatus;
  href: string;
}

