on:
  push:
    branches:
      - main

name: Increment Tag

env:
  TAG: v1.0.0

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Determine commit message
        id: commit
        run: |
          COMMIT_MESSAGE=$(git log --format=%B -n 1 ${{ github.sha }})
          echo "::set-output name=message::${COMMIT_MESSAGE}"

      - name: Increment tag based on commit message
        id: increment-tag
        run: |
          TAG_TYPE=$(echo "${{ steps.commit.outputs.message }}" | cut -d' ' -f1)
          if [[ "${TAG_TYPE}" == "feat" ]]; then
            TAG=$(echo "${TAG}" | awk -F. '{$NF = $NF + 1;} 1' OFS=. | sed 's/.$//')
          elif [[ "${TAG_TYPE}" == "fix" ]]; then
            TAG=$(echo "${TAG}" | awk -F. '{$(NF-1) = $(NF-1) + 1;} 1' OFS=. | sed 's/.$//')
          fi
          echo "::set-output name=tag::${TAG}"

      - name: Update environment variable
        run: |
          echo "TAG=${{ steps.increment-tag.outputs.tag }}" >> $GITHUB_ENV

      # Continue with your remaining build steps using the updated TAG value
