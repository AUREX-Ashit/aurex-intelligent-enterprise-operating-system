"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { Card, CardDescription, CardTitle } from "@/components/ui/Card";
import { FormBanner, FormField, FormLabel } from "@/components/ui/Form";
import { useEstablishRole } from "@/features/role/state/useEstablishRole";

export function RoleManagementScreen() {
  const { state, establish } = useEstablishRole();
  const [roleCode, setRoleCode] = useState("");
  const [roleName, setRoleName] = useState("");
  const [description, setDescription] = useState("");
  const [isSystemRole, setIsSystemRole] = useState(false);
  const isLoading = state.status === "establishing";

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    establish({
      role_code: roleCode,
      role_name: roleName,
      description: description || null,
      is_system_role: isSystemRole,
    });
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Roles & Permissions</h1>
        <p className="mt-1 text-sm text-muted-foreground">Establish Business or System Roles (C-003).</p>
      </div>

      <Card>
        <CardTitle>Establish Role</CardTitle>
        <CardDescription>
          No list/search endpoint exists yet for Role (WP-02 did not build one) — this screen
          covers establishment only.
        </CardDescription>

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <FormField>
              <FormLabel htmlFor="role-code">Role Code</FormLabel>
              <Input id="role-code" value={roleCode} onChange={(event) => setRoleCode(event.target.value)} required disabled={isLoading} />
            </FormField>

            <FormField>
              <FormLabel htmlFor="role-name">Role Name</FormLabel>
              <Input id="role-name" value={roleName} onChange={(event) => setRoleName(event.target.value)} required disabled={isLoading} />
            </FormField>
          </div>

          <FormField>
            <FormLabel htmlFor="role-description">Description</FormLabel>
            <Input
              id="role-description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              disabled={isLoading}
              placeholder="Optional"
            />
          </FormField>

          <FormField>
            <FormLabel>Role Kind</FormLabel>
            <div className="flex gap-2">
              <Button type="button" variant={!isSystemRole ? "primary" : "secondary"} onClick={() => setIsSystemRole(false)} disabled={isLoading}>
                Business Role
              </Button>
              <Button type="button" variant={isSystemRole ? "primary" : "secondary"} onClick={() => setIsSystemRole(true)} disabled={isLoading}>
                System Role
              </Button>
            </div>
          </FormField>

          <Button type="submit" disabled={isLoading}>
            {isLoading && <Spinner className="mr-2" />}
            Establish Role
          </Button>
        </form>

        {state.status === "error" && (
          <div className="mt-4">
            <FormBanner tone="danger">
              {state.isConflict ? "A Role with this role_code already exists." : state.message}
            </FormBanner>
          </div>
        )}

        {state.status === "established" && (
          <div className="mt-4">
            <FormBanner tone="success">
              Role {state.role.role_name} ({state.role.role_code}) established — version {state.role.version}.
            </FormBanner>
          </div>
        )}
      </Card>
    </div>
  );
}
