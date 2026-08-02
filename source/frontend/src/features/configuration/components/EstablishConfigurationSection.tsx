"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardTitle, CardDescription } from "@/components/ui/Card";
import { FormBanner, FormField, FormHelperText, FormLabel } from "@/components/ui/Form";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import type { ConfigurationEstablishState } from "@/features/configuration/state/useConfigurationManagement";
import type { ConfigurationFacet, EstablishConfigurationEntryRequest } from "@/types/configuration";

const FACETS: ConfigurationFacet[] = ["TERMINOLOGY", "BRANDING", "THEME", "ACCESSIBILITY", "LOCALIZATION"];

// DS-001 §11.3's own closed, five-class Theme Model — White-label excluded
// (IRA-010 §4.3, same root cause as dual-logo Branding).
const THEME_CLASSES = ["LIGHT", "DARK", "HIGH_CONTRAST", "BOARDROOM"];
const ACCESSIBILITY_KEYS = ["high_contrast_enabled", "reduced_motion_enabled"];
const BOOLEAN_VALUES = ["true", "false"];

function defaultKeyForFacet(facet: ConfigurationFacet): string {
  switch (facet) {
    case "THEME":
      return "theme_class";
    case "BRANDING":
      return "logo_url";
    case "LOCALIZATION":
      return "default_language";
    case "ACCESSIBILITY":
      return ACCESSIBILITY_KEYS[0];
    case "TERMINOLOGY":
      return "";
  }
}

export function EstablishConfigurationSection({
  state,
  onEstablish,
}: {
  state: ConfigurationEstablishState;
  onEstablish: (request: EstablishConfigurationEntryRequest) => void;
}) {
  const [facet, setFacet] = useState<ConfigurationFacet>("THEME");
  const [key, setKey] = useState(defaultKeyForFacet("THEME"));
  const [themeClass, setThemeClass] = useState(THEME_CLASSES[0]);
  const [booleanValue, setBooleanValue] = useState(BOOLEAN_VALUES[0]);
  const [textValue, setTextValue] = useState("");
  const isLoading = state.status === "establishing";

  function selectFacet(next: ConfigurationFacet) {
    setFacet(next);
    setKey(defaultKeyForFacet(next));
    setTextValue("");
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    let value: unknown = textValue;
    if (facet === "THEME") value = themeClass;
    if (facet === "ACCESSIBILITY") value = booleanValue === "true";

    onEstablish({ facet, key, value });
  }

  return (
    <Card>
      <CardTitle>Establish Configuration</CardTitle>
      <CardDescription>
        Sets a tenant-wide override for your Organization. Resolves ahead of the platform default the next
        time any screen requests this Configuration (WP-10 BA-02, EX-C041-02).
      </CardDescription>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <FormField>
          <FormLabel>Facet</FormLabel>
          <div className="flex flex-wrap gap-2">
            {FACETS.map((f) => (
              <Button
                key={f}
                type="button"
                variant={facet === f ? "primary" : "secondary"}
                onClick={() => selectFacet(f)}
                disabled={isLoading}
              >
                {f}
              </Button>
            ))}
          </div>
        </FormField>

        {facet === "TERMINOLOGY" && (
          <FormField>
            <FormLabel htmlFor="configuration-key">Term key</FormLabel>
            <Input
              id="configuration-key"
              value={key}
              onChange={(event) => setKey(event.target.value)}
              placeholder="e.g. role.ceo"
              required
              disabled={isLoading}
            />
            <FormHelperText>The vocabulary key this Organization overrides, e.g. a role or field label.</FormHelperText>
          </FormField>
        )}

        {facet === "ACCESSIBILITY" && (
          <FormField>
            <FormLabel>Accessibility flag</FormLabel>
            <div className="flex gap-2">
              {ACCESSIBILITY_KEYS.map((k) => (
                <Button
                  key={k}
                  type="button"
                  variant={key === k ? "primary" : "secondary"}
                  onClick={() => setKey(k)}
                  disabled={isLoading}
                >
                  {k}
                </Button>
              ))}
            </div>
          </FormField>
        )}

        <FormField>
          <FormLabel>Value</FormLabel>
          {facet === "THEME" && (
            <div className="flex flex-wrap gap-2">
              {THEME_CLASSES.map((cls) => (
                <Button
                  key={cls}
                  type="button"
                  variant={themeClass === cls ? "primary" : "secondary"}
                  onClick={() => setThemeClass(cls)}
                  disabled={isLoading}
                >
                  {cls}
                </Button>
              ))}
            </div>
          )}
          {facet === "ACCESSIBILITY" && (
            <div className="flex gap-2">
              {BOOLEAN_VALUES.map((v) => (
                <Button
                  key={v}
                  type="button"
                  variant={booleanValue === v ? "primary" : "secondary"}
                  onClick={() => setBooleanValue(v)}
                  disabled={isLoading}
                >
                  {v}
                </Button>
              ))}
            </div>
          )}
          {(facet === "BRANDING" || facet === "LOCALIZATION" || facet === "TERMINOLOGY") && (
            <Input
              value={textValue}
              onChange={(event) => setTextValue(event.target.value)}
              placeholder={
                facet === "BRANDING" ? "https://…/logo.png" : facet === "LOCALIZATION" ? "e.g. en, fr, de" : "Override label"
              }
              required
              disabled={isLoading}
            />
          )}
        </FormField>

        <Button type="submit" disabled={isLoading || (facet === "TERMINOLOGY" && key.trim().length === 0)}>
          {isLoading && <Spinner className="mr-2" />}
          Establish Configuration
        </Button>
      </form>

      {state.status === "establish-error" && (
        <div className="mt-4">
          <FormBanner tone="danger">{state.message}</FormBanner>
        </div>
      )}

      {state.status === "established" && (
        <div className="mt-4">
          <FormBanner tone="success">
            {state.entry.facet} &ldquo;{state.entry.key}&rdquo; established — version {state.entry.version}.
          </FormBanner>
        </div>
      )}
    </Card>
  );
}
