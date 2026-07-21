"use client";

import { useEffect, useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { Spinner } from "@/components/ui/Spinner";
import { FormBanner } from "@/components/ui/Form";
import { useEstablishOrganization } from "@/features/organization/state/useEstablishOrganization";
import { useViewOrganization } from "@/features/organization/state/useViewOrganization";
import { useUpdateOrganization } from "@/features/organization/state/useUpdateOrganization";
import { EstablishOrganizationForm } from "@/features/organization/components/EstablishOrganizationForm";
import { OrganizationDetailsList } from "@/features/organization/components/OrganizationDetailsList";
import { OrganizationSearchGrid } from "@/features/organization/components/OrganizationSearchGrid";
import { UpdateOrganizationForm } from "@/features/organization/components/UpdateOrganizationForm";
import { ViewOrganizationSection } from "@/features/organization/components/ViewOrganizationSection";
import type { OrganizationResponse } from "@/types/organization";

/**
 * WP-01 Business Activities implemented: BA-01 Establish Organization,
 * BA-02 View Organization Details, BA-03 Search & List Organizations
 * (the primary Organization Management screen — the grid below), BA-04
 * Update Organization Profile. Remaining Business Activities
 * (Activate/Suspend, Configuration, Audit History — IRA-001 §9) extend
 * this screen as they land; this is not a stand-in for the full
 * capability.
 */
export function OrganizationManagementScreen() {
  const { state: establishState, establish, reset: resetEstablish } = useEstablishOrganization();
  // Two independent instances — the grid's per-row "View Details" modal and
  // the standalone by-ID lookup section below must not share one state, or
  // opening one would leak its result into the other's display.
  const { state: viewModalState, view: viewInModal, reset: resetViewModal } = useViewOrganization();
  const { state: standaloneViewState, view: viewStandalone } = useViewOrganization();
  const { state: updateState, update, reset: resetUpdate } = useUpdateOrganization();

  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isViewOpen, setIsViewOpen] = useState(false);
  const [editingOrganization, setEditingOrganization] = useState<OrganizationResponse | null>(null);
  const [gridRefreshKey, setGridRefreshKey] = useState(0);

  // Close the Create modal and refresh the grid once establish succeeds.
  useEffect(() => {
    if (establishState.status === "established") {
      setIsCreateOpen(false);
      setGridRefreshKey((key) => key + 1);
    }
  }, [establishState]);

  // Close the Edit modal and refresh the grid once update succeeds.
  useEffect(() => {
    if (updateState.status === "updated") {
      setEditingOrganization(null);
      setGridRefreshKey((key) => key + 1);
    }
  }, [updateState]);

  function openCreateModal() {
    resetEstablish();
    setIsCreateOpen(true);
  }

  function openViewModal(organization: OrganizationResponse) {
    setIsViewOpen(true);
    viewInModal(organization.id);
  }

  function openEditModal(organization: OrganizationResponse) {
    resetUpdate();
    setEditingOrganization(organization);
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Organization Management</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Search, create, and review organizations. Requires the PLATFORM_ADMIN role.
        </p>
      </div>

      <OrganizationSearchGrid
        key={gridRefreshKey}
        onCreateOrganization={openCreateModal}
        onViewOrganization={openViewModal}
        onEditOrganization={openEditModal}
      />

      <Modal open={isCreateOpen} onClose={() => setIsCreateOpen(false)} title="Establish Organization">
        {/* No result panel here: on success this modal closes and the grid
            refreshes immediately (see the effect above), so a "no results
            yet" panel would only ever be visible mid-typing, before
            there's anything to show. */}
        <EstablishOrganizationForm state={establishState} onEstablish={establish} />
      </Modal>

      <Modal
        open={isViewOpen}
        onClose={() => {
          setIsViewOpen(false);
          resetViewModal();
        }}
        title="Organization Details"
      >
        {viewModalState.status === "loading" && (
          <div className="flex items-center justify-center py-8">
            <Spinner />
          </div>
        )}
        {viewModalState.status === "not-found" && <FormBanner tone="warning">No organization exists with this ID.</FormBanner>}
        {viewModalState.status === "error" && <FormBanner tone="danger">{viewModalState.message}</FormBanner>}
        {viewModalState.status === "found" && <OrganizationDetailsList organization={viewModalState.organization} />}
      </Modal>

      <Modal
        open={editingOrganization !== null}
        onClose={() => setEditingOrganization(null)}
        title="Update Organization Profile"
      >
        {editingOrganization && (
          <UpdateOrganizationForm
            organization={editingOrganization}
            state={updateState}
            onUpdate={(fields) => update(editingOrganization.id, fields)}
          />
        )}
      </Modal>

      <ViewOrganizationSection state={standaloneViewState} onView={viewStandalone} />
    </div>
  );
}
