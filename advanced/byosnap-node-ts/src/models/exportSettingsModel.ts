// models/exportSettingsModel.ts

import { SettingsSchema } from './settingsModel';

export interface ExportSettingsSchema {
  version: string;
  exported_at: number;
  data: {
    [environment: string]: {
      [toolId: string]: SettingsSchema;
    };
  };
}
