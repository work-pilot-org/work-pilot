export function getBaseDomainUrl(path: string = "") {
  if (typeof window === "undefined") return path;

  const hostname = window.location.hostname;
  const port = window.location.port ? `:${window.location.port}` : "";
  const protocol = window.location.protocol;

  let baseDomain = hostname;
  
  if (hostname.includes(".localhost")) {
    baseDomain = "localhost";
  } else if (hostname.includes(".workpilot.com")) {
    baseDomain = "workpilot.com";
  }

  return `${protocol}//${baseDomain}${port}${path}`;
}

export function getTenantDomainUrl(domain: string, path: string = "") {
  if (typeof window === "undefined") return path;

  const hostname = window.location.hostname;
  const port = window.location.port ? `:${window.location.port}` : "";
  const protocol = window.location.protocol;

  let baseDomain = hostname;
  if (hostname.includes(".localhost")) {
    baseDomain = "localhost";
  } else if (hostname.includes(".workpilot.com")) {
    baseDomain = "workpilot.com";
  }

  return `${protocol}//${domain}.${baseDomain}${port}${path}`;
}

export function isSubdomain() {
  if (typeof window === "undefined") return false;
  const hostname = window.location.hostname;
  
  if (hostname.includes(".localhost")) return true;
  if (hostname.includes(".workpilot.com")) {
    const parts = hostname.split(".");
    return parts.length > 2 && parts[0] !== "www";
  }
  return false;
}