// models/settingsModel.ts

export interface SettingsComponent {
  id: string;
  type: string;
  value: string;
}

export interface SettingsSection {
  id: string;
  components: SettingsComponent[];
}

export interface SettingsSchema {
  sections: SettingsSection[];
}

export function getDefaultSettings(): SettingsSchema {
  return {
    sections: [
      {
        id: 'registration',
        components: [
          {
            id: 'characters',
            type: 'textarea',
            value: '',
          },
        ],
      },
    ],
  };
}
