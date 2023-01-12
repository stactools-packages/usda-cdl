# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project attempts to match the major and minor versions of [stactools](https://github.com/stac-utils/stactools) and increments the patch number as needed.

## [Unreleased]

## [0.1.2] - 2023-01-12

### Fixed

- Frequency tiles now use `mode` for their overview resampling ([#16](https://github.com/stactools-packages/usda-cdl/issues/16))

## [0.1.1] - 2023-01-06

### Added

- `usda_cdl:type` to the collection summaries ([#14](https://github.com/stactools-packages/usda-cdl/pull/14))

### Fixed

- Location of `usda_cdl:type` (it was at the top level, but needed to be in properties).

## [0.1.0] - 2022-12-22

Initial release

[Unreleased]: <https://github.com/stactools-packages/usda-cdl/compare/v0.1.2...main>
[0.1.2]: <https://github.com/stactools-packages/usda-cdl/compare/v0.1.1...v0.1.2>
[0.1.1]: <https://github.com/stactools-packages/usda-cdl/compare/v0.1.0...v0.1.1>
[0.1.0]: <https://github.com/stactools-packages/usda-cdl/tree/v0.1.0>
