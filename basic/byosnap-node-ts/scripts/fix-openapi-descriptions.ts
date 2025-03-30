import fs from 'fs';
import path from 'path';

// Path to your generated swagger.json (adjust if needed)
const swaggerPath = path.resolve(__dirname, '../snapser-resources/swagger.json');

if (!fs.existsSync(swaggerPath)) {
  console.error(`❌ swagger.json not found at: ${swaggerPath}`);
  process.exit(1);
}

const swagger = JSON.parse(fs.readFileSync(swaggerPath, 'utf-8'));

for (const pathKey in swagger.paths) {
  const pathItem = swagger.paths[pathKey];
  for (const methodKey of Object.keys(pathItem)) {
    const operation = pathItem[methodKey];
    if (operation['x-description'] && !operation['description']) {
      operation['description'] = operation['x-description'];
      delete operation['x-description'];
    }
  }
}

fs.writeFileSync(swaggerPath, JSON.stringify(swagger, null, 2));
console.log('✅ Swagger description fields updated using x-description.');
