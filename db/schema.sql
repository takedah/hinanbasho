DROP TABLE IF EXISTS evacuation_sites;
CREATE TABLE evacuation_sites(
  id SERIAL NOT NULL,
  site_id integer NOT NULL PRIMARY KEY,
  site_name TEXT NOT NULL,
  postal_code VARCHAR(8),
  address TEXT,
  phone_number VARCHAR(16),
  latitude decimal NOT NULL,
  longitude decimal NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX ON evacuation_sites (site_id);
DROP TABLE IF EXISTS area_addresses;
CREATE TABLE area_addresses(
  id SERIAL NOT NULL,
  postal_code CHAR(8) NOT NULL PRIMARY KEY,
  area_name TEXT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX ON area_addresses (postal_code);
