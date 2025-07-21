{{- define "mariadb.name" -}}
mariadb
{{- end }}

{{- define "mariadb.fullname" -}}
{{ .Release.Name }}-{{ include "mariadb.name" . }}
{{- end }}